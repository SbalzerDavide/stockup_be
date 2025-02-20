

import dataclasses
import datetime
from typing import TYPE_CHECKING

from . import models

if TYPE_CHECKING:
  from .models import ShoppingList


@dataclasses.dataclass
class ShoppingListDataClass:
  name: str
  description: str = None
  is_active: bool = True
  is_purchased: bool = False
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None
  
  @classmethod
  def from_instance(cls, shopping_list_model: "ShoppingList") -> "ShoppingListDataClass":
    return cls(
      id=shopping_list_model.id,
      name=shopping_list_model.name,
      created_at=shopping_list_model.created_at,
      updated_at=shopping_list_model.updated_at
    )
    
def create_shopping_list(user, shopping_list_dc: "ShoppingListDataClass") -> "ShoppingListDataClass":
  shopping_list = models.ShoppingList.objects.create(
    user=user,
    name=shopping_list_dc.name,
    description=shopping_list_dc.description,
    is_active=shopping_list_dc.is_active,
    is_purchased=shopping_list_dc.is_purchased
  )
  return ShoppingListDataClass.from_instance(shopping_list)    
    
def get_shopping_lists(user) -> "ShoppingListDataClass":
  shoppingLists = models.ShoppingList.objects.filter(user=user)
  return [ShoppingListDataClass.from_instance(shopping_list) for shopping_list in shoppingLists]