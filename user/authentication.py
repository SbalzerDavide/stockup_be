# from django.conf import settings
from rest_framework import authentication, exceptions
import jwt

import os
from dotenv import load_dotenv



from . import models

class UserAuthentication(authentication.BaseAuthentication):
  def authenticate(self, request):
    token = request.COOKIES.get('jwt')
    
    load_dotenv()
    jwt_secret = os.getenv('JWT_SECRET')

    
    if not token:
      return None
    
    try:
      payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
    except :
      raise exceptions.AuthenticationFailed('Unauthenticated')
    
    user = models.User.objects.filter(id=payload['id']).first()
    
    return (user, None)
