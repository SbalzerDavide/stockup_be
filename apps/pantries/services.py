
import dataclasses
import datetime

from user import models as UserModel

from .models import Pantry as PantryModel
@dataclasses.dataclass
class PantriesDataClass:
  id: int = None
  # user_id: int = None
  name: str = None
  description: str = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None

  @classmethod
  def from_instance(cls, pantry_model: "PantryModel") -> "PantriesDataClass":
    return cls(
      id=pantry_model.id,
      # user_id=pantry_model.user_id,
      name=pantry_model.name,
      description=pantry_model.description,
      created_at=pantry_model.created_at,
      updated_at=pantry_model.updated_at
    )
        
def get_pantries(user) -> list["PantriesDataClass"]:
  return [PantriesDataClass.from_instance(pantry) for pantry in PantryModel.objects.filter(user=user)]
  
def create_pantry(user: "UserModel", pantry_dc: "PantriesDataClass") -> "PantriesDataClass":
  pantry_create = PantryModel.objects.create(
    user=user,
    name=pantry_dc.name,
    description=pantry_dc.description
  )
  return PantriesDataClass.from_instance(pantry_create)