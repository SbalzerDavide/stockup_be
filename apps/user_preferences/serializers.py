from rest_framework import serializers
from user import serializers as user_serializers

from . import services

class UserPreferencesSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  # user_id = serializers.IntegerField()
  preference_type = serializers.CharField()
  value = serializers.CharField()
  user = user_serializers.UserSerializer(read_only=True)
  created_at = serializers.DateTimeField(read_only=True)
  updated_at = serializers.DateTimeField(read_only=True)
  
  def to_internal_value(self, data):
    data = super().to_internal_value(data)
    
    return services.UserPreferencesDataClass(**data)