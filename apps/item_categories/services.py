import dataclasses 
import datetime
from typing import TYPE_CHECKING

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