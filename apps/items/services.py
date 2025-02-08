import dataclasses
import datetime

from typing import TYPE_CHECKING

from .models import Items


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
  items_create = Items.objects.create(
    name=item_dc.name,
    consumation_average_days=item_dc.consumation_average_days,
    department=item_dc.department,
    is_edible=item_dc.is_edible,
    category=item_dc.category,
    user=user
  )
  return ItemDataClass.from_instance(items_create)