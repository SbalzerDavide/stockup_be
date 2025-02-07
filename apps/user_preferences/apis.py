from rest_framework import views
from rest_framework import permissions
from rest_framework import response

from user import authentication
from . import serializers
from . import services

class UserPreferencesListApi(views.APIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  
  def post(self, request):
    serializer = serializers.UserPreferencesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    
    # create user preferences
    serializer.instance = services.create_user_preferences(user=request.user, user_preferences_dc=data)
    
    return response.Response(data=serializer.data)

  def get(self, request):
    user_preferences = services.get_user_preferences(user=request.user)
    serializer = serializers.UserPreferencesSerializer(user_preferences, many=True)
    
    return response.Response(data=serializer.data)
  
class UserPreferencesDetailApi(views.APIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  
  def get(self, request, user_preferences_id):
    user_preferences = services.get_user_preferences_by_id(user_preferences_id=user_preferences_id)
    serializer = serializers.UserPreferencesSerializer(user_preferences)
    
    return response.Response(data=serializer.data)
  
  def put(self, request, user_preferences_id):
    serializer = serializers.UserPreferencesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    
    # update user preferences
    serializer.instance = services.update_user_preferences(user=request.user, user_preferences_id=user_preferences_id, user_preferences_dc=data)
    
    return response.Response(data=serializer.data)
  
  def delete(self, request, user_preferences_id):
    services.delete_user_preferences(user=request.user, user_preferences_id=user_preferences_id)
    
    return response.Response(status=204)
  
