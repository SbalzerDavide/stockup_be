import dataclasses
import datetime
import json
from django.shortcuts import get_object_or_404

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate

from typing import TYPE_CHECKING

from .models import Items

from user.models import User as UserModel

from apps.item_categories import services as service_categorires
from apps.item_categories.models import ItemCategories

from apps.item_macronutriments import services as service_macronutriments
from apps.item_macronutriments.models import ItemMacronutriments

from apps.llm.models import llm

if TYPE_CHECKING:
  from .models import Items 

@dataclasses.dataclass
class ItemDataClass:
  name: str
  category: str = None
  macronutriments: str = None
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
      macronutriments=items_model.macronutriments,
      consumation_average_days=items_model.consumation_average_days,
      department=items_model.department,
      is_edible=items_model.is_edible,
      created_at=items_model.created_at,
      updated_at=items_model.updated_at
    )    
    
def create_item(user, item_dc: "ItemDataClass") -> "ItemDataClass":
  proposed_category = auto_set_category(name=item_dc.name, user=user)
  proposed_is_edible = auto_set_is_edible(name=item_dc.name)
  proposed_department = auto_set_department(name=item_dc.name)
  proposed_macronutriments = auto_set_macronutriments(name=item_dc.name)
  print(proposed_macronutriments)
  items_create = Items.objects.create(
    name=item_dc.name,
    category= proposed_category,
    macronutriments=proposed_macronutriments,
    consumation_average_days=item_dc.consumation_average_days,
    department=proposed_department,
    is_edible=proposed_is_edible,
    user=user
  )
  return ItemDataClass.from_instance(items_create)

def get_items(user: "UserModel") -> list["ItemDataClass"]:
  items = Items.objects.filter(user=user)
  return [ItemDataClass.from_instance(single_item) for single_item in items]

def auto_set_category(name: str, user) -> 'ItemCategories':
  categories = service_categorires.get_item_categories(user)
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
  parse_json(response.content)
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

def auto_set_is_edible(name: str) -> bool:
  response_schemas = [
    ResponseSchema(name="is_edible", description="Definisce se un prodotto è commestibile o meno")
  ]
  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
  prompt_template = PromptTemplate(
    template=(
        "Ti fornirò il nome di un prodotto acquistabile al supermercato."
        "Il tuo compito è assegnare assegnare il valore true se il prodotto è edibile e false se non lo è.\n\n"
        "Prodotto: {product}\n"
        "{format_instructions}\n"
        "Devi sempre restituire un JSON valido racchiuso da un blocco di codice markdown. Non restituire alcun testo aggiuntivo."

    ),
    input_variables=["product", "categories"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
  )
  formatted_prompt = prompt_template.format(
    product=name,
  )
  response = llm.invoke(formatted_prompt)
  parse_json(response.content)

  structured_output = output_parser.parse(response.content)
  if 'is_edible' not in structured_output:
    return None
  return structured_output['is_edible']

def auto_set_department(name: str) -> str:
  response_schemas = [
    ResponseSchema(name="department", description="Definisce il reparto del supermercato in cui trovare un prodotto")
  ]
  departments = ['Frutta e verdura', 'Macelleria', 'Pescheria', 'Salumeria', 'Panetteria', 'Pasticceria', 'Latticini', 'Surgelati', 'Pasta e riso', 'Conserve', 'Bevande', 'Igiene', 'Pulizia', 'Alcolici', 'Caffè e tè', 'Dolci', 'Snack', 'Cereali', 'Piatti pronti', 'Cibo per animali', 'Altro']
  departments_string = ', '.join(department for department in departments)

  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
  prompt_template = PromptTemplate(
    template=(
        "Ti fornirò il nome di un prodotto acquistabile al supermercato e una lista reparti del supermercato. "
        "Il tuo compito è assegnare il prodotto al reparto in cu isi può trovare più appropriata dalla lista.\n\n"
        "Prodotto: {product}\n"
        "reparti: {departments_string}\n\n"
        "Devi sempre restituire un JSON valido racchiuso da un blocco di codice markdown. Non restituire alcun testo aggiuntivo."
        "{format_instructions}\n"
        "Devi sempre restituire un JSON valido racchiuso da un blocco di codice markdown. Non restituire alcun testo aggiuntivo."
    ),
    input_variables=["product", "categories"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
  )
  formatted_prompt = prompt_template.format(
    product=name,
    departments_string=departments_string
  )
  response = llm.invoke(formatted_prompt)
  parse_json(response.content)

  structured_output = output_parser.parse(response.content)
  if 'department' not in structured_output:
    return None
  return structured_output['department']

def auto_set_macronutriments(name: str) -> 'ItemMacronutriments':
  macronutriments = service_macronutriments.get_item_macronutriments()
  mapped_macronutriments = [{'summary': f"{macronutriment.name} {macronutriment.description}" , 'id': macronutriment.id} for macronutriment in macronutriments]

  response_schemas = [
    ResponseSchema(name="macronutriment", description="Definisce il macronutrimente più apprpriato per il prodotto rispetto alla lista fornita")
  ]
  output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
  prompt_template = PromptTemplate(
    template=(
        "Ti fornirò il nome di un prodotto acquistabile al supermercato e un array di macronutrimenti.\n\n"
        "Al prodotto deve essere abbinato una tipologia di macronutrimenti rispetto alle sue proprotà nutrizionali.\n\n"
        "Il tuo compito è assegnare il prodotto alla tipologia di macronutirimenti più appropriata dalla lista.\n\n"
        "Prodotto: {product}\n"
        "Tipologie di macronutrimenti disponibili: {macronutriments}\n\n"
        "{format_instructions}\n"
        "Devi sempre restituire un JSON valido racchiuso da un blocco di codice markdown. Non restituire alcun testo aggiuntivo."
    ),
    input_variables=["product", "macronutriments"],
    partial_variables={"format_instructions": output_parser.get_format_instructions()},
  )
  formatted_prompt = prompt_template.format(
    product=name,
    macronutriments=json.dumps(mapped_macronutriments),
  )
  response = llm.invoke(formatted_prompt)
  parse_json(response.content)
  structured_output = output_parser.parse(response.content)
  if(not structured_output.get('macronutriment')):
    return None
  for item in mapped_macronutriments:
    if item['id'] == structured_output['macronutriment']:
        proposed_macronutriment_id = item['id']
        break 
    else:
      proposed_macronutriment_id = None
  if not proposed_macronutriment_id:
    return None
  return get_object_or_404(ItemMacronutriments, pk=proposed_macronutriment_id)

def parse_json(string):
  try:
    return json.loads(string)
  except:
    return string