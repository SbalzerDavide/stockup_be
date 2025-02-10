from django.urls import path

from . import apis

urlpatterns = [
  path('item-categories/', apis.ItemCategoryListApi.as_view(), name='preferences'),
  path('item-categories/<int:item_category_id>/', apis.ItemCategoryDetailApi.as_view(), name='preferences'),
]