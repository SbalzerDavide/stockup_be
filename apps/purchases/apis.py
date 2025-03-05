from rest_framework import views, response, permissions

from user import authentication
from . import serializers
from . import services

class PurchasesListApi(views.APIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)

  def post(self, request):
    serializer = serializers.PurchaseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    
    # create purchase
    serializer.instance = services.create_purchase(user=request.user, purchase_dc=data)
    return response.Response(data=serializer.data)

  def get(self, request):
    purchases = services.get_purchases(user=request.user)
    serializer = serializers.PurchaseSerializer(purchases, many=True)
    
    return response.Response(data=serializer.data)