from rest_framework import serializers

from . import services
from user.serializers import UserSerializer
from apps.item_categories.serializers import ItemCategorySerializer

class ItemSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  user = UserSerializer(read_only=True)
  category = ItemCategorySerializer(read_only=True, required=False)
  name = serializers.CharField()
  consumation_average_days = serializers.FloatField(required=False) # from LLM
  department = serializers.CharField(required=False) # from LLM
  is_edible = serializers.BooleanField(required=False) # from LLM
  created_at = serializers.DateTimeField(read_only=True)
  updated_at = serializers.DateTimeField(read_only=True)
  
  def to_internal_value(self, data):
    data = super().to_internal_value(data)
    
    return services.ItemDataClass(**data)