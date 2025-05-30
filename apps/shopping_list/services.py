import dataclasses 
import datetime
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404

from .models import ShoppingList as ShoppingListModel

if TYPE_CHECKING:
  from .models import ShoppingList

@dataclasses.dataclass
class ShoppingListDataClass:
  name: str
  description: str = None
  is_active: bool = None
  is_purchased: bool = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None
  
  @classmethod
  def from_instance(cls, shopping_list_model: "ShoppingList") -> "ShoppingListDataClass":
    if shopping_list_model is None:
        raise ValueError("Cannot create DataClass from None object")
    return cls(
      id=shopping_list_model.id,
      name=shopping_list_model.name,
      description=shopping_list_model.description,
      is_active=shopping_list_model.is_active,
      is_purchased=shopping_list_model.is_purchased,
      created_at=shopping_list_model.created_at,
      updated_at=shopping_list_model.updated_at
    )
    
def create_shopping_list(user, shopping_list_dc: "ShoppingListDataClass") -> "ShoppingListDataClass":
  print(user)
  shopping_list = ShoppingListModel.objects.create(
    name=shopping_list_dc.name,
    description=shopping_list_dc.description,
    is_active=shopping_list_dc.is_active,
    is_purchased=shopping_list_dc.is_purchased,
    user=user
  )
  return ShoppingListDataClass.from_instance(shopping_list)    
    
def get_shopping_lists(user):
  return ShoppingListModel.objects.filter(user=user)

def get_shopping_lists_as_dataclasses(user):
  shopping_lists = get_shopping_lists(user)
  return [ShoppingListDataClass.from_instance(shopping_list) for shopping_list in shopping_lists]

def update_shopping_list(id: int, shopping_list_item_dc):
    """
    Aggiorna una lista della spesa esistente con dati grezzi.
    
    Args:
        id: ID della lista della spesa da aggiornare
        shopping_list_item_dc: Dizionario con i dati grezzi dalla richiesta
    """    
    # Recupera l'oggetto esistente
    shopping_list = get_object_or_404(ShoppingListModel, pk=id)
    
    # Aggiorna solo i campi presenti nei dati ricevuti
    if 'name' in shopping_list_item_dc:
        shopping_list.name = shopping_list_item_dc['name']
    
    if 'description' in shopping_list_item_dc:
        shopping_list.description = shopping_list_item_dc['description']
    
    if 'is_active' in shopping_list_item_dc:
        shopping_list.is_active = shopping_list_item_dc['is_active']
    
    if 'is_purchased' in shopping_list_item_dc:
        shopping_list.is_purchased = shopping_list_item_dc['is_purchased']
    
    # Salva le modifiche
    shopping_list.save()
    
    # Restituisce l'oggetto aggiornato come DataClass
    return shopping_list