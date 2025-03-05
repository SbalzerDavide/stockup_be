from rest_framework import serializers

from . import services

from apps.shopping_list.serializers import ShoppingListSerializer

class PurchaseSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  user = serializers.IntegerField(read_only=True)
  
  shopping_list = ShoppingListSerializer(read_only=True, required=False)
  shopping_list_id = serializers.IntegerField()
  
  total_cost = serializers.FloatField()
  total_items = serializers.IntegerField()
  
  store = serializers.CharField(max_length=255)
  purchase_date = serializers.DateTimeField()
  
  created_at = serializers.DateTimeField(read_only=True)
  updated_at = serializers.DateTimeField(read_only=True)
  
  def to_internal_value(self, data):
    data = super().to_internal_value(data)
    
    return services.PurchaseDataClass(**data)