from rest_framework import views, response, permissions

from user import authentication

from . import serializers
from . import services

class PantriesListApi(views.APIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  
  def post(self, request):
    serializer = serializers.PantiresSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    
    # create pantry
    serializer.instance = services.create_pantry(user=request.user, pantry_dc=data)
    return response.Response(data=serializer.data)
  
  def get(self, request):
    pantries = services.get_pantries(user=request.user)
    serializer = serializers.PantiresSerializer(pantries, many=True)
    
    return response.Response(data=serializer.data)
