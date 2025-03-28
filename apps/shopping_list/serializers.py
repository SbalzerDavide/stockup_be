from rest_framework import serializers


from user.serializers import UserSerializer

from . import services


class ShoppingListSerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  user = UserSerializer(read_only=True)
  
  name = serializers.CharField()
  description = serializers.CharField(max_length=255, required=False)
  
  is_active = serializers.BooleanField(default=True)
  is_purchased = serializers.BooleanField(default=False)
  
  created_at = serializers.DateTimeField(read_only=True)
  updated_at = serializers.DateTimeField(read_only=True)

  def to_internal_value(self, data):
    data = super().to_internal_value(data)
    
    return services.ShoppingListDataClass(**data)