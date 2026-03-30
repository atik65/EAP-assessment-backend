from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# =============================================================================
# API ROUTER CONFIGURATION — Module B2
# =============================================================================

# Create a router and register viewsets
router = DefaultRouter()

# Register Category and Product ViewSets
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

# =============================================================================
# URL PATTERNS
# =============================================================================

urlpatterns = [
    # Include all router-generated URLs
    # This creates the following endpoints:
    # - GET    /api/categories/          - List all categories
    # - POST   /api/categories/          - Create a category
    # - GET    /api/categories/{id}/     - Get category details
    # - PATCH  /api/categories/{id}/     - Update category
    # - DELETE /api/categories/{id}/     - Delete category
    # 
    # - GET    /api/products/            - List all products
    # - POST   /api/products/            - Create a product
    # - GET    /api/products/{id}/       - Get product details
    # - PATCH  /api/products/{id}/       - Update product
    # - DELETE /api/products/{id}/       - Archive product (soft delete)
    path('api/', include(router.urls)),
]

