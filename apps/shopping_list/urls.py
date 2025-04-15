from django.urls import path

from . import apis
urlpatterns = [
    path('shopping-lists/', apis.ShoppingListsListApi.as_view(), name='shopping-lists'),
    path('shopping-lists/<int:shopping_list_id>/', apis.ShoppingListDetailApi.as_view(), name='shopping-list-detail'),
]