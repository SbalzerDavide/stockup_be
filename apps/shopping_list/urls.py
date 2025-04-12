from django.urls import path

from . import apis
urlpatterns = [
    path('shopping-lists/', apis.ShoppingListsListApi.as_view(), name='shopping-lists'),
]