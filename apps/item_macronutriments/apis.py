from rest_framework import views, response, permissions

from user import authentication
from . import serializers
from . import services

class ItemMacronutrimentsListApi(views.APIView):
  def post(self, request):
    serializer = serializers.ItemMacronutrimentsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    # create item macronutriments
    serializer.instance = services.create_item_macronutriments(item_macronutriments_dc=data)

    return response.Response(data=serializer.data)

  def get(self, request):
    item_macronutriments = services.get_item_macronutriments()
    serializer = serializers.ItemMacronutrimentsSerializer(item_macronutriments, many=True)

    return response.Response(data=serializer.data)