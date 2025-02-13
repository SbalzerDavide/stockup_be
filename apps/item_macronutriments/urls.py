from django.urls import path

from . import apis

urlpatterns = [
  path('item-macronutriments/', apis.ItemMacronutrimentsListApi.as_view(), name='item-macronutriments'),
  # path('item-macronutriments/<int:item_macronutriments_id>/', apis.ItemMacronutrimentsDetailApi.as_view(), name='item-macronutriments_detail'),
]