from rest_framework import views, response, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from user import authentication
from . import serializers
from . import services

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ItemListApi(generics.ListCreateAPIView):
    authentication_classes = (authentication.UserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_edible', 'department', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at', 'updated_at', 'consumation_average_days']
    ordering = ['-created_at']  # ordinamento predefinito
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        return services.get_items(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        serializer.instance = services.create_item(user=request.user, item_dc=data)
        return response.Response(data=serializer.data)