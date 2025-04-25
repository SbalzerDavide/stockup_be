from django.urls import path

from . import apis

urlpatterns = [
  path('items/', apis.ItemListApi.as_view(), name='items'),
  path('items/<int:item_id>/', apis.ItemDetailApi.as_view(), name='items_detail')
]