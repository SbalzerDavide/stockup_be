from django.urls import path

from . import apis

urlpatterns = [
  path('items/', apis.ItemListApi.as_view(), name='items'),
  # path('items/<int:items_id>/', apis.ItemsDetailApi.as_view(), name='items_detail')
]