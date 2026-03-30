"""
URL Configuration for Order API — Module B3

Endpoints:
- GET    /api/orders/              - List orders (with filtering)
- POST   /api/orders/              - Create order
- GET    /api/orders/{id}/         - Get order detail
- PATCH  /api/orders/{id}/status/  - Update order status
- POST   /api/orders/{id}/cancel/  - Cancel order
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
