from django.urls import path

from . import apis
urlpatterns = [
    path('shopping_lists/', apis.ShoppingListsListApi.as_view(), name='shopping_lists'),
]