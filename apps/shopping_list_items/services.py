

import dataclasses
import datetime
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404

from user.models import User as UserModel

from apps.items import services as item_services
from apps.items.models import Items as ItemModel 

from apps.shopping_list import services as shopping_list_services

from .models import ShoppingListItems

if TYPE_CHECKING:
  from .models import ShoppingListItems 


@dataclasses.dataclass
class ShoppingListItemDataClass:
  is_checked: bool
  is_proposed: bool
  quantity: int
  item: item_services.ItemDataClass = None
  item_id: str = None
  shopping_list_id: str = None
  shopping_list: shopping_list_services.ShoppingListDataClass = None
  weight: float = None
  unit_weight: str = None
  volume: float = None
  unit_volume: str = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None
  
  @classmethod
  def from_instance(cls, shopping_list_items_model: "ShoppingListItems") -> "ShoppingListItemDataClass":
    return cls(
      id=shopping_list_items_model.id,
      is_checked=shopping_list_items_model.is_checked,
      is_proposed=shopping_list_items_model.is_proposed,
      item=shopping_list_items_model.item,
      item_id=shopping_list_items_model.item_id,
      shopping_list_id=shopping_list_items_model.shopping_list_id,
      shopping_list=shopping_list_items_model.shopping_list,
      quantity=shopping_list_items_model.quantity,
      weight=shopping_list_items_model.weight,
      unit_weight=shopping_list_items_model.unit_weight,
      volume=shopping_list_items_model.volume,
      unit_volume=shopping_list_items_model.unit_volume,
      created_at=shopping_list_items_model.created_at,
      updated_at=shopping_list_items_model.updated_at
    )
    
def create_shopping_list_item(user: "UserModel", shopping_list_item_dc: "ShoppingListItemDataClass") -> "ShoppingListItemDataClass":
  item = get_object_or_404(ItemModel, pk=shopping_list_item_dc.item_id)
  shopping_list_item_create = ShoppingListItems.objects.create(
    item=item,
    shopping_list_id=shopping_list_item_dc.shopping_list_id,
    is_checked=shopping_list_item_dc.is_checked,
    is_proposed=shopping_list_item_dc.is_proposed,
    quantity=shopping_list_item_dc.quantity,
    weight=shopping_list_item_dc.weight,
    unit_weight=shopping_list_item_dc.unit_weight,
    volume=shopping_list_item_dc.volume,
    unit_volume=shopping_list_item_dc.unit_volume,
    user=user,
  )
  return ShoppingListItemDataClass.from_instance(shopping_list_item_create)
    
def get_shopping_list_items(user: "UserModel") -> list["ShoppingListItemDataClass"]:
  shoppingListItems = ShoppingListItems.objects.filter(user=user)
  return [ShoppingListItemDataClass.from_instance(shopping_list_item) for shopping_list_item in shoppingListItems]