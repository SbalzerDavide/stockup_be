from rest_framework import views, response, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from user import authentication

from . import serializers
from . import services
from .models import ShoppingList

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ShoppingListsListApi(generics.ListCreateAPIView):
  authentication_classes = (authentication.UserAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  pagination_class = StandardResultsSetPagination
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filterset_fields = ['created_at', 'updated_at']
  search_fields = ['name']
  ordering_fields = ['name', 'created_at', 'updated_at']
  ordering = ['-created_at']  # default ordering
  serializer_class = serializers.ShoppingListSerializer

  def get_queryset(self):
    return ShoppingList.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)