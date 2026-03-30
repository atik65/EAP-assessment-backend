from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging

from .models import ExampleModel
from .serializers import (
    ExampleModelSerializer,
    ExampleDetailSerializer,
    ExampleCreateUpdateSerializer
)

logger = logging.getLogger(__name__)


# Example ViewSet - Replace with your own views
class ExampleModelViewSet(viewsets.ModelViewSet):
    """
    Example ViewSet to demonstrate Django REST Framework ViewSet structure.
    
    Provides CRUD operations for ExampleModel:
    - list: GET /api/examples/
    - create: POST /api/examples/
    - retrieve: GET /api/examples/{id}/
    - update: PUT /api/examples/{id}/
    - partial_update: PATCH /api/examples/{id}/
    - destroy: DELETE /api/examples/{id}/
    
    Replace this with your own viewsets.
    """
    queryset = ExampleModel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Return different serializers for different actions.
        """
        if self.action == 'list':
            return ExampleModelSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ExampleCreateUpdateSerializer
        else:
            return ExampleDetailSerializer

    @extend_schema(
        summary="Get active items",
        description="Returns only active items",
        responses={200: ExampleModelSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='active')
    def active_items(self, request):
        """
        Example custom action to get only active items.
        Accessible at: GET /api/examples/active/
        """
        queryset = self.get_queryset().filter(is_active=True)
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Toggle item status",
        description="Toggle the is_active status of an item"
    )
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """
        Example custom action on a single item.
        Accessible at: POST /api/examples/{id}/toggle_status/
        """
        item = self.get_object()
        item.is_active = not item.is_active
        item.save()
        serializer = self.get_serializer(item)
        return Response(serializer.data)


# Example function-based API view
@extend_schema(
    summary="Health check",
    description="Check if the API is running"
)
@api_view([ 'GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Example function-based view for health check.
    Accessible at: GET /api/health/
    """
    return Response({
        'status': 'healthy',
        'message': 'API is running',
        'version': '1.0.0'
    })


@extend_schema(
    summary="Get statistics",
    description="Get statistics about the data"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statistics(request):
    """
    Example function-based view for statistics.
    Accessible at: GET /api/statistics/
    """
    stats = {
        'total_items': ExampleModel.objects.count(),
        'active_items': ExampleModel.objects.filter(is_active=True).count(),
        'inactive_items': ExampleModel.objects.filter(is_active=False).count(),
    }
    
    return Response(stats)
