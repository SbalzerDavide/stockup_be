from django.urls import include, path

from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user import apis

router = routers.DefaultRouter()

urlpatterns = [
  path('register', apis.RegisterApi.as_view(), name='register'),
  path('login', apis.loginApi.as_view(), name='login'),
  path('me', apis.userApi.as_view(), name='me'),
  path('logout', apis.logoutApi.as_view(), name='logout'),
]