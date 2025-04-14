from django.urls import path

from . import apis

urlpatterns = [
  path('shopping_list_items/', apis.ShoppingListItemListApi.as_view(), name='shopping_list_items'),
  path('shopping_list_items/<int:shopping_list_item_id>/', apis.ShoppingListItemDetailApi.as_view(), name='shopping_list_item_detail'),
]