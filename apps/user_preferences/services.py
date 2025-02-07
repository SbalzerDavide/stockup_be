import dataclasses 
import datetime
from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404
from . import models as user_preferences_models
from user.models import User as UserModel

from user import services as user_services

if TYPE_CHECKING:
  from .models import UserPreferences


@dataclasses.dataclass
class UserPreferencesDataClass:
  preference_type: str
  value: str
  # user_id: int = None
  user: user_services.UserDataClass = None
  created_at: datetime.datetime = None
  updated_at: datetime.datetime = None
  id: int = None
  
  @classmethod
  def from_instance(cls, user_preferences_model: "UserPreferences") -> "UserPreferencesDataClass":
    return cls(
      # user_id=user_preferences_model.user_id,
      id=user_preferences_model.id,
      preference_type=user_preferences_model.preference_type,
      value=user_preferences_model.value,
      # user=user_services.UserDataClass.from_instance(user_preferences_model.user),
      user=user_preferences_model.user,
      created_at=user_preferences_model.created_at,
      updated_at=user_preferences_model.updated_at
    )
    
def create_user_preferences(user, user_preferences_dc: "UserPreferencesDataClass") -> "UserPreferencesDataClass":
  user_preferences_create = user_preferences_models.UserPreferences.objects.create(
    preference_type=user_preferences_dc.preference_type,
    value=user_preferences_dc.value,
    user=user
  )
  return UserPreferencesDataClass.from_instance(user_preferences_create)
  
def get_user_preferences(user: "UserModel") -> list["UserPreferencesDataClass"]:
  user_preferences = user_preferences_models.UserPreferences.objects.filter(user=user)
  return [UserPreferencesDataClass.from_instance(single_user_preferences) for single_user_preferences in user_preferences]

def get_user_preferences_by_id(user_preferences_id: int) -> "UserPreferencesDataClass":
  user_preferences = get_object_or_404(user_preferences_models.UserPreferences, pk=user_preferences_id)

  return UserPreferencesDataClass.from_instance(user_preferences) 

def update_user_preferences(user: "UserModel", user_preferences_id: int, user_preferences_dc: "UserPreferencesDataClass") -> "UserPreferencesDataClass":
  user_preferences = get_object_or_404(user_preferences_models.UserPreferences, pk=user_preferences_id)
  if user.id != user_preferences.user_id:
    raise ValueError("User does not have permission to update this user preferences")
  user_preferences.preference_type = user_preferences_dc.preference_type
  user_preferences.value = user_preferences_dc.value
  user_preferences.save()
  return UserPreferencesDataClass.from_instance(user_preferences)

def delete_user_preferences(user: "UserModel", user_preferences_id: int):
  user_preferences = get_object_or_404(user_preferences_models.UserPreferences, pk=user_preferences_id)
  if user.id != user_preferences.user_id:
    raise ValueError("User does not have permission to delete this user preferences")
  user_preferences.delete()
  
