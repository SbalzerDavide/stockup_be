from django.urls import path

from . import apis

urlpatterns = [
  path('item-categories/', apis.ItemCategoryListApi.as_view(), name='preferences'),
]