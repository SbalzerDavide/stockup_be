from django.urls import path

from . import apis

urlpatterns = [
  path('pantries/', apis.PantriesListApi.as_view(), name='pantries'),
  # path('pantries/<int:pantry_id>/', apis.ItemDetailApi.as_view(), name='items_detail')
]