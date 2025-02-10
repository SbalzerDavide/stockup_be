import dataclasses
import datetime
import json
from django.shortcuts import get_object_or_404

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate

from typing import TYPE_CHECKING

from .models import Items

from apps.item_categories import services as model_categorires
from apps.item_categories.models import ItemCategories

from apps.llm.models import llm

if TYPE_CHECKING:
  from .models import Items 

@dataclasses.dataclass
class ItemDataClass:
  name: str
  category: str = None
  consumation_average_days: float = None
  department: str = None
  is_edible: bool = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None
  
  @classmethod
  def from_instance(cls, items_model: "Items") -> "ItemDataClass":
    return cls(
      id=items_model.id,
      name=items_model.name,
      category=items_model.category,
      consumation_average_days=items_model.consumation_average_days,
      department=items_model.department,
      is_edible=items_model.is_edible,
      created_at=items_model.created_at,
      updated_at=items_model.updated_at
    )    
    
def create_item(user, item_dc: "ItemDataClass") -> "ItemDataClass":
  proposed_category = autoSetCategory(name=item_dc.name, user=user)
  items_create = Items.objects.create(
    name=item_dc.name,
    category= proposed_category,
    consumation_average_days=item_dc.consumation_average_days,
    department=item_dc.department,
    is_edible=item_dc.is_edible,
    user=user
  )
  return ItemDataClass.from_instance(items_create)

def autoSetCategory(name: str, user) -> 'ItemCategories':
  categories = model_categorires.get_item_categories(user)
  mapped_category = [{'name': category.name, 'id': category.id} for category in categories]
  categories_string = ', '.join(category['name'] for category in mapped_category)

  response_schemas = [
    ResponseSchema(name="category", description="Categoria del prodotto, selezionata dall'elenco fornito")
  ]
  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
  prompt_template = PromptTemplate(
    template=(
        "Ti fornirò il nome di un prodotto acquistabile al supermercato e una lista di categorie. "
        "Il tuo compito è assegnare il prodotto alla categoria più appropriata dalla lista.\n\n"
        "Prodotto: {product}\n"
        "Categorie disponibili: {categories}\n\n"
        "{format_instructions}"
    ),
    input_variables=["product", "categories"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
  )
  formatted_prompt = prompt_template.format(
    product=name,
    categories=categories_string,
  )
  response = llm.invoke(formatted_prompt)
  try:
    structured_output = response.json()
  except json.JSONDecodeError:
    print("Errore: Risposta non è un JSON valido")
    return None
  structured_output = output_parser.parse(response.content)
  if(not structured_output.get('category')):
    return None
  for item in mapped_category:
    if item['name'].lower() == structured_output['category'].lower():
        proposed_category_id = item['id']
        break 
    else:
      proposed_category_id = None
  proposed_category_id = next((item['id'] for item in mapped_category if item['name'].lower() == structured_output['category'].lower()), None)
  if not proposed_category_id:
    return None
  return get_object_or_404(ItemCategories, pk=proposed_category_id)