from rest_framework import views, response, exceptions, permissions

from . import services
from . import authentication

from user import serializers as user_serializers
class RegisterApi(views.APIView):
  def post(self, request):
    serializer = user_serializers.UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    data = serializer.validated_data
    
    serializer.instance = services.create_user(user_dc = data)
        
    return response.Response(data=serializer.data)
  
class loginApi(views.APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']
    
    user = services.user_email_selector(email=email)
    
    if user is None:
      raise exceptions.AuthenticationFailed('User not found')
   
    if not user.check_password(raw_password=password):
      raise exceptions.AuthenticationFailed('Incorrect password')
    
    token = services.create_token(user_id=user.id)
    
    serializer = user_serializers.UserSerializer(user)
    response_data = serializer.data
    response_data['token'] = token
    resp = response.Response(data=response_data)
    
    resp.set_cookie(key='jwt', value=token, httponly=True)

    return resp
    
class userApi(views.APIView):
  """
  This endpoit is only use if the user is authenticated
  """
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  
  def get(self, request):
    user = request.user
    
    serializer = user_serializers.UserSerializer(user)
    return response.Response(serializer.data)
  
class logoutApi(views.APIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)  
  
  def post(self, request):
    resp = response.Response()
    
    resp.delete_cookie(key='jwt')
    resp.data = {'message': 'succesfully logged out'}
    return resp