import dataclasses
import datetime
import json
from django.shortcuts import get_object_or_404
from pydantic import BaseModel

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
  category: service_categorires.ItemCategoriesDataClass = None
  macronutriments: service_macronutriments.ItemMacronutrimentsDataClass = None
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
  class StructuredOutput(BaseModel) : 
    category: str

  structuredLlm = llm.with_structured_output(StructuredOutput);
  prompt = f"Ti fornirò il nome di un prodotto acquistabile al supermercato e una lista di categorie. Il tuo compito è assegnare il prodotto alla categoria più appropriata dalla lista.\n\n Prodotto: {name}\n Categorie disponibili: {categories_string}\n\n"        

  response = structuredLlm.invoke(prompt);
  if not response.category:
    return None
  for item in mapped_category:
    if item['name'].lower() == response.category.lower():
        proposed_category_id = item['id']
        break 
    else:
      proposed_category_id = None
  if not proposed_category_id:
    return None
  return get_object_or_404(ItemCategories, pk=proposed_category_id)

def auto_set_is_edible(name: str) -> bool:
  class StructuredOutput(BaseModel) : 
    is_edible: bool

  structuredLlm = llm.with_structured_output(StructuredOutput);
  prompt = f"Ti fornirò il nome di un prodotto acquistabile al supermercato. \n Il tuo compito è assegnare assegnare il valore true se il prodotto è edibile e false se non lo è.\n\n Prodotto: {name}\n\n Devi sempre restituire un JSON valido racchiuso da un blocco di codice markdown. Non restituire alcun testo aggiuntivo."
  response = structuredLlm.invoke(prompt)
  if not hasattr(response, 'is_edible'):
    return None
  return response.is_edible

def auto_set_department(name: str) -> str:
  departments = ['Frutta e verdura', 'Macelleria', 'Pescheria', 'Salumeria', 'Panetteria', 'Pasticceria', 'Latticini', 'Surgelati', 'Pasta e riso', 'Conserve', 'Bevande', 'Igiene', 'Pulizia', 'Alcolici', 'Caffè e tè', 'Dolci', 'Snack', 'Cereali', 'Piatti pronti', 'Cibo per animali', 'Altro']
  departments_string = ', '.join(department for department in departments)
  
  class StructuredOutput(BaseModel) : 
    department: str
    
  prompt = f"Ti fornirò il nome di un prodotto acquistabile al supermercato e una lista reparti del supermercato.\n Il tuo compito è assegnare il prodotto al reparto in cu isi può trovare più appropriata dalla lista.\n\n Prodotto: {name}\n reparti: {departments_string}\n\n Devi sempre restituire un JSON valido racchiuso da un blocco di codice markdown. Non restituire alcun testo aggiuntivo."
  structuredLlm = llm.with_structured_output(StructuredOutput);

  response = structuredLlm.invoke(prompt)
  if not response.department:
    return None
  return response.department

def auto_set_macronutriments(name: str) -> 'ItemMacronutriments':
  macronutriments = service_macronutriments.get_item_macronutriments()
  mapped_macronutriments = [{'summary': f"{macronutriment.name} {macronutriment.description}" , 'id': macronutriment.id} for macronutriment in macronutriments]
  
  class StructuredOutput(BaseModel) : 
    macronutriment: int
    
  prompt = f"Ti fornirò il nome di un prodotto acquistabile al supermercato e un array di macronutrimenti.\n\n Al prodotto deve essere abbinato una tipologia di macronutrimenti rispetto alle sue proprotà nutrizionali.\n\n Il tuo compito è assegnare il prodotto alla tipologia di macronutirimenti più appropriata dalla lista.\n\n Prodotto: {name}\n Tipologie di macronutrimenti disponibili: {json.dumps(mapped_macronutriments)}\n\n"
  structuredLlm = llm.with_structured_output(StructuredOutput);

  response = structuredLlm.invoke(prompt)
  if not response.macronutriment:
    return None
  
  for item in mapped_macronutriments:
    if item['id'] == response.macronutriment:
        proposed_macronutriment_id = item['id']
        break 
    else:
      proposed_macronutriment_id = None
  if not proposed_macronutriment_id:
    return None
  return get_object_or_404(ItemMacronutriments, pk=proposed_macronutriment_id)
