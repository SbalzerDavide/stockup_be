from rest_framework import serializers

from . import services

class ItemCategorySerializer(serializers.Serializer):
  id = serializers.IntegerField(read_only=True)
  name = serializers.CharField()
  description = serializers.CharField(required=False)
  created_at = serializers.DateTimeField(read_only=True)
  updated_at = serializers.DateTimeField(read_only=True)
  
  def to_internal_value(self, data):
    data = super().to_internal_value(data)
    
    return services.ItemCategoriesDataClass(**data)