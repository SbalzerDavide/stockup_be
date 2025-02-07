from django.urls import path

from . import apis

urlpatterns = [
  path('preferences/', apis.UserPreferencesListApi.as_view(), name='preferences'),
  path('preferences/<int:user_preferences_id>/', apis.UserPreferencesDetailApi.as_view(), name='preferences_detail')
]