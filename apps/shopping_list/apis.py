from rest_framework import views, response, permissions

from user import authentication

from . import serializers
from . import services

class ShoppingListsListApi(views.APIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)

  def post(self, request):
    serializer = serializers.ShoppingListSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    # create shoping list
    serializer.instance = services.create_shopping_list(user=request.user, shopping_list_dc=data)
    return response.Response(data=serializer.data)

  def get(self, request):
    items = services.get_shopping_lists(user=request.user)
    serializer = serializers.ShoppingListSerializer(items, many=True)

    return response.Response(data=serializer.data)