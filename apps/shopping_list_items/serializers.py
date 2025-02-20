from rest_framework import serializers

from apps.shopping_list.serializers import ShoppingListSerializer

from . import services
from . import models

from apps.items.serializers import ItemSerializer
from user.serializers import UserSerializer



class ShoppingListItemSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  user = UserSerializer(read_only=True)
  
  item = ItemSerializer(read_only=True, required=False)
  item_id = serializers.IntegerField(required=False)
  
  shopping_list_id = serializers.IntegerField(required=False)
  shopping_list = ShoppingListSerializer(read_only=True, required=False)
  
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
  
  # example of how to override the to_representation method 
  # for field to show in the sesponse
  # def to_representation(self, instance):
  #   rapresentation =  super().to_representation(instance)
  #   item = rapresentation.get('item')
  #   cleaned_item = {
  #     "id": item.get('id'),
  #     "name": item.get('name'),
  #     "department": item.get('department'),
  #   }
  #   return {
  #     'id': rapresentation.get('id'),
  #     'user': rapresentation.get('user'),
  #     # 'item': rapresentation.get('item'),
  #     'item': cleaned_item,
  #     'item_id': rapresentation.get('item_id'),
  #     'is_checked': rapresentation.get('is_checked'),
  #     'is_proposed': rapresentation.get('is_proposed'),
  #     'quantity': rapresentation.get('quantity'),
  #     'volume': rapresentation.get('volume'),
  #     'weight': rapresentation.get('weight'),
  #     # 'unit_volume': rapresentation.get('unit_volume'),
  #     # 'unit_weight': rapresentation.get('unit_weight'),
  #     # 'created_at': rapresentation.get('created_at'),
  #     # 'updated_at': rapresentation.get('updated_at')
  #   }
  
 