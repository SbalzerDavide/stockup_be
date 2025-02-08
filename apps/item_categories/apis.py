from rest_framework import views, response, permissions

from user import authentication
from . import serializers
from . import services

class ItemCategoryListApi(views.APIView):
    authentication_classes = (authentication.UserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = serializers.ItemCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # create item category
        serializer.instance = services.create_item_category(user = request.user, item_category_dc=data)

        return response.Response(data=serializer.data)

    def get(self, request):
        item_categories = services.get_item_categories(user=request.user)
        serializer = serializers.ItemCategorySerializer(item_categories, many=True)

        return response.Response(data=serializer.data)