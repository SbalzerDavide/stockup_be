import dataclasses
import datetime
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404

from apps.shopping_list import services as shopping_list_services
from apps.shopping_list.models import ShoppingList

from user import models as UserModel

from .models import Purchase as PurchaseModel


if TYPE_CHECKING:
  from .models import Purchase as PurchaseModel

@dataclasses.dataclass
class PurchaseDataClass:
  shopping_list_id: int
  shopping_list = shopping_list_services.ShoppingListDataClass = None
  total_cost: float
  total_items: int
  store: str
  purchase_date: datetime.datetime
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None
  
  @classmethod
  def from_instance(cls, purchase_model: "PurchaseModel") -> "PurchaseDataClass":
    print(purchase_model.shopping_list)
    return cls(
      id=purchase_model.id,
      shopping_list_id=purchase_model.shopping_list_id,
      # shopping_list=purchase_model.shopping_list,
      total_cost=purchase_model.total_cost,
      total_items=purchase_model.total_items,
      store=purchase_model.store,
      purchase_date=purchase_model.purchase_date,
      created_at=purchase_model.created_at,
      updated_at=purchase_model.updated_at
    )
    
def create_purchase(user: "UserModel", purchase_dc: "PurchaseDataClass") -> "PurchaseDataClass":
  shopping_list = get_object_or_404(ShoppingList, pk=purchase_dc.shopping_list_id)
  purchase_create = PurchaseModel.objects.create(
    user=user,
    shopping_list_id=purchase_dc.shopping_list_id,
    shopping_list=shopping_list,
    total_cost=purchase_dc.total_cost,
    total_items=purchase_dc.total_items,
    store=purchase_dc.store,
    purchase_date=purchase_dc.purchase_date,
  )
  return PurchaseDataClass.from_instance(purchase_create)  
    
def get_purchases(user: "UserModel") -> list["PurchaseDataClass"]:
  return [PurchaseDataClass.from_instance(purchase) for purchase in PurchaseModel.objects.filter(user=user)]