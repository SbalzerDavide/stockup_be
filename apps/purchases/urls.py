
from django.urls import path
from . import apis

urlpatterns = [
  path('purchases/', apis.PurchasesListApi.as_view(), name='purchases'),
]