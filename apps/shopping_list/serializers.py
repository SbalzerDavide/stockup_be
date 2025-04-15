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
    return serializer.data