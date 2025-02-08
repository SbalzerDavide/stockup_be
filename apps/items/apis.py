from rest_framework import views, response, permissions

from user import authentication
from . import serializers
from . import services

class ItemListApi(views.APIView):
    authentication_classes = (authentication.UserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = serializers.ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # create item
        serializer.instance = services.create_item(user=request.user, item_dc=data)

        return response.Response(data=serializer.data)

    # def get(self, request):
    #     items = services.get_items(user=request.user)
    #     serializer = serializers.ItemSerializer(items, many=True)

    #     return response.Response(data=serializer.data)