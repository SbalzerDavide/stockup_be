from rest_framework import serializers

from user.serializers import UserSerializer
from . import services
from .models import ShoppingList

class ShoppingListSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  
  class Meta:
    model = ShoppingList
    fields = ['id', 'user', 'name', 'description', 'is_active', 'is_purchased', 'created_at', 'updated_at']
    read_only_fields = ['id', 'user', 'created_at', 'updated_at']