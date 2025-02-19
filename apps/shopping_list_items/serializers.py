from rest_framework import serializers

from . import services

from apps.items.serializers import ItemSerializer
from user.serializers import UserSerializer



class ShoppingListItemSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  user = UserSerializer(read_only=True)
  item = ItemSerializer(read_only=True, required=False)
  
  item_id = serializers.IntegerField()
  
  is_checked = serializers.BooleanField(default=False)  
  is_proposed = serializers.BooleanField(default=False) 
  
  quantity = serializers.IntegerField(default=1)
  
  volume = serializers.FloatField(required=False)
  weight = serializers.FloatField(required=False)
  unit_volume = serializers.CharField(max_length=255, required=False)
  unit_weight = serializers.CharField(max_length=255, required=False)
  
  created_at = serializers.DateTimeField(read_only=True)
  updated_at = serializers.DateTimeField(read_only=True)
  
  def to_internal_value(self, data):
    data = super().to_internal_value(data)
    
    return services.ShoppingListItemDataClass(**data)