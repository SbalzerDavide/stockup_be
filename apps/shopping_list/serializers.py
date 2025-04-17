from rest_framework import serializers

from user.serializers import UserSerializer
from . import services
from .models import ShoppingList

class ShoppingListSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  items = serializers.SerializerMethodField()
  
  class Meta:
    model = ShoppingList
    fields = ['id', 'user', 'name', 'description', 'is_active', 'is_purchased', 'created_at', 'updated_at', 'items']
    read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'items']
    
  def get_items(self, obj):
    from apps.shopping_list_items.models import ShoppingListItems
    from apps.shopping_list_items.serializers import ShoppingListItemSerializer
    
    items = ShoppingListItems.objects.filter(shopping_list=obj)
    serializer = ShoppingListItemSerializer(items, many=True)
    items_data = serializer.data
    
    # customization of the representation
    custom_items = []
    for item in items_data:
      # Seleziona solo i campi che vuoi includere
      custom_item = {
        'id': item.get('id'),
        'item_name': item.get('item', {}).get('name') if item.get('item') else None,
        'macronutriments': item.get('item', {}).get('macronutrients') if item.get('item') else None,
        'category': item.get('item', {}).get('category') if item.get('item') else None,
        'department': item.get('item', {}).get('department') if item.get('item') else None,
        'item_id': item.get('item_id'),
        'is_checked': item.get('is_checked'),
        'is_proposed': item.get('is_proposed'),
        'quantity': item.get('quantity'),
        'weight': item.get('weight'),
        'unit_weight': item.get('unit_weight'),
        'volume': item.get('volume'),
        'unit_volume': item.get('unit_volume'),
      }
      
      # add optional fields only if they exist
      if item.get('weight'):
        custom_item['weight'] = item.get('weight')
        custom_item['unit_weight'] = item.get('unit_weight')
        
      if item.get('volume'):
        custom_item['volume'] = item.get('volume')
        custom_item['unit_volume'] = item.get('unit_volume')
        
      custom_items.append(custom_item)
    
    return custom_items