import dataclasses 
import datetime
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404

from user.models import User as UserModel

from .models import ItemCategories as ItemCategoriesModel

if TYPE_CHECKING:
  from .models import ItemCategories
  
@dataclasses.dataclass
class ItemCategoriesDataClass:
  name: str
  description: str = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None
  
  @classmethod
  def from_instance(cls, item_categories_model: "ItemCategories") -> "ItemCategoriesDataClass":
    return cls(
      id=item_categories_model.id,
      name=item_categories_model.name,
      description=item_categories_model.description,
      created_at=item_categories_model.created_at,
      updated_at=item_categories_model.updated_at
    ) 
    
def create_item_category(user, item_category_dc: "ItemCategoriesDataClass") -> "ItemCategoriesDataClass":
  item_categories_create = ItemCategoriesModel.objects.create(
    name=item_category_dc.name,
    description=item_category_dc.description,
    user=user
  )
  return ItemCategoriesDataClass.from_instance(item_categories_create)

def get_item_categories(user: "UserModel") -> list["ItemCategoriesDataClass"]:
  item_categories = ItemCategoriesModel.objects.filter(user=user)
  return [ItemCategoriesDataClass.from_instance(single_item_categories) for single_item_categories in item_categories]

def get_item_category_by_id(item_category_id: int) -> "ItemCategoriesDataClass":
  item_categories = get_object_or_404(ItemCategoriesModel, pk=item_category_id)

  return ItemCategoriesDataClass.from_instance(item_categories)

def update_item_category(item_category_id: int, item_category_dc: "ItemCategoriesDataClass") -> "ItemCategoriesDataClass":
  item_categories = get_object_or_404(ItemCategoriesModel, pk=item_category_id)
  item_categories.name = item_category_dc.name
  item_categories.description = item_category_dc.description
  
  item_categories.consumation_average_days = item_category_dc.consumation_average_days
  item_categories.department = item_category_dc.department
  item_categories.is_edible = item_category_dc.is_edible

  item_categories.save()
  
  return ItemCategoriesDataClass.from_instance(item_categories)

def delete_item_category(item_category_id: int):
  item_categories = get_object_or_404(ItemCategoriesModel, pk=item_category_id)
  print(item_categories)
  item_categories.delete()