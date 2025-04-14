from rest_framework import views, response, permissions

from user import authentication
from . import serializers
from . import services


class ShoppingListItemListApi(views.APIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)

  def post(self, request):
    serializer = serializers.ShoppingListItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    # create shoping list item
    serializer.instance = services.create_shopping_list_item(user=request.user, shopping_list_item_dc=data)
    return response.Response(data=serializer.data)

  def get(self, request):
    items = services.get_shopping_list_items(user=request.user)
    serializer = serializers.ShoppingListItemSerializer(items, many=True)

    return response.Response(data=serializer.data)
  
class ShoppingListItemDetailApi(views.APIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request, shopping_list_item_id):
    shopping_list_item = services.get_shopping_list_item(shopping_list_item_id=shopping_list_item_id)
    serializer = serializers.ShoppingListItemSerializer(shopping_list_item)
    return response.Response(data=serializer.data)
