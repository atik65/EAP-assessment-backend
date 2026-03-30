"""
Views for Order management — Module B3

This module provides REST API endpoints for:
- Listing orders with filtering (status, date, customer search)
- Creating orders with multiple items (atomic transaction)
- Retrieving order details
- Updating order status (with transition validation)
- Cancelling orders (with stock restoration)
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Order, OrderItem
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer
)
from products.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Order management.
    
    Endpoints:
    - GET /api/orders/ - List orders with filtering
    - POST /api/orders/ - Create order with items
    - GET /api/orders/{id}/ - Get order detail
    - PATCH /api/orders/{id}/status/ - Update order status
    - POST /api/orders/{id}/cancel/ - Cancel order and restore stock
    
    Query Parameters (for list):
    - ?status=pending|confirmed|shipped|delivered|cancelled
    - ?created_at__date=YYYY-MM-DD
    - ?search=customer_name
    - ?ordering=-created_at
    """
    
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filtering
    filterset_fields = ['status']
    
    # Search
    search_fields = ['customer_name', 'order_number']
    
    # Ordering
    ordering_fields = ['created_at', 'total_price', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action.
        
        - list: OrderListSerializer (with item_count)
        - retrieve: OrderDetailSerializer (with full items)
        - create: OrderCreateSerializer (for order creation)
        - status: OrderStatusUpdateSerializer (for status updates)
        """
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        elif self.action == 'update_status':
            return OrderStatusUpdateSerializer
        return OrderDetailSerializer
    
    def get_queryset(self):
        """
        Optimize queryset with select_related and prefetch_related.
        
        For list view: basic optimization
        For detail view: prefetch items with products
        """
        queryset = super().get_queryset()
        
        if self.action == 'list':
            # For list view, just count items efficiently
            queryset = queryset.select_related('created_by')
        elif self.action == 'retrieve':
            # For detail view, prefetch all items with products
            queryset = queryset.prefetch_related(
                'items',
                'items__product'
            )
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Create a new order with multiple items.
        
        Request body:
        {
            "customer_name": "John Doe",
            "items": [
                {"product_id": "uuid", "quantity": 2},
                {"product_id": "uuid", "quantity": 1}
            ]
        }
        
        Response (201 Created):
        - Full order detail with items
        
        Errors (400 Bad Request):
        - Duplicate products in order
        - Product not found
        - Product not active
        - Insufficient stock
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Return full order detail
        detail_serializer = OrderDetailSerializer(order)
        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        """
        Update order status with transition validation.
        
        PATCH /api/orders/{id}/status/
        
        Request body:
        {
            "status": "confirmed"
        }
        
        Response (200 OK):
        - Full order detail
        
        Errors (400 Bad Request):
        - Invalid status transition
        """
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(
            order,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return full order detail
        detail_serializer = OrderDetailSerializer(order)
        return Response(detail_serializer.data)
    
    @action(detail=True, methods=['post'], url_path='cancel')
    @transaction.atomic
    def cancel(self, request, pk=None):
        """
        Cancel an order and restore stock for all items.
        
        POST /api/orders/{id}/cancel/
        
        Response (200 OK):
        {
            "message": "Order cancelled successfully. Stock restored for all items.",
            "order": { ... full order detail ... }
        }
        
        Errors (400 Bad Request):
        - Order is already cancelled
        - Order is in a terminal state (delivered)
        - Invalid status transition
        """
        order = self.get_object()
        
        # Validate that we can cancel from current status
        if not order.can_transition_to(Order.STATUS_CANCELLED):
            return Response(
                {
                    'detail': f"Cannot cancel order with status '{order.status}'. "
                              f"Invalid status transition."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Restore stock for all items
        for order_item in order.items.all():
            product = order_item.product
            product.stock_quantity += order_item.quantity
            product.save()  # This triggers status update and restock queue check
        
        # Update order status to cancelled
        order.status = Order.STATUS_CANCELLED
        order.save()
        
        # Return success response
        detail_serializer = OrderDetailSerializer(order)
        return Response({
            'message': 'Order cancelled successfully. Stock restored for all items.',
            'order': detail_serializer.data
        })

