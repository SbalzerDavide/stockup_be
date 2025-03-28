import dataclasses
import datetime
from typing import TYPE_CHECKING

from .models import ItemMacronutriments

if TYPE_CHECKING:
    from .models import ItemMacronutriments

@dataclasses.dataclass
class ItemMacronutrimentsDataClass:
  name: str
  description: str = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None

  @classmethod
  def from_instance(cls, item_macronutriments_model: "ItemMacronutriments") -> "ItemMacronutrimentsDataClass":
    return cls(
      id=item_macronutriments_model.id,
      name=item_macronutriments_model.name,
      description=item_macronutriments_model.description,
      created_at=item_macronutriments_model.created_at,
      updated_at=item_macronutriments_model.updated_at
    )

def create_item_macronutriments(item_macronutriments_dc: "ItemMacronutrimentsDataClass") -> "ItemMacronutrimentsDataClass":
  item_macronutriments_create = ItemMacronutriments.objects.create(
    name=item_macronutriments_dc.name,
    description=item_macronutriments_dc.description
  )
  return ItemMacronutrimentsDataClass.from_instance(item_macronutriments_create)

def get_item_macronutriments() -> list["ItemMacronutrimentsDataClass"]:
  item_macronutriments = ItemMacronutriments.objects.all()
  return [ItemMacronutrimentsDataClass.from_instance(single_item_macronutriments) for single_item_macronutriments in item_macronutriments]