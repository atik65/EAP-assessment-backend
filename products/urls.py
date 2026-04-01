from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# =============================================================================
# API ROUTER CONFIGURATION — Modules B2, B4 & B6
# =============================================================================

# Create a router and register viewsets
router = DefaultRouter()

# Module B2: Register Category and Product ViewSets
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"products", views.ProductViewSet, basename="product")

# Module B4: Register Restock Queue ViewSet
router.register(r"restock", views.RestockQueueViewSet, basename="restock")

# =============================================================================
# URL PATTERNS
# =============================================================================

urlpatterns = [
    # Include all router-generated URLs
    # This creates the following endpoints:
    #
    # Module B2 — Categories & Products:
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
    #
    # Module B4 — Restock Queue:
    # - GET    /api/restock/             - List restock queue
    # - GET    /api/restock/{id}/        - Get restock queue entry details
    # - POST   /api/restock/{id}/restock/ - Restock a product (add stock)
    # - DELETE /api/restock/{id}/        - Manually remove from queue
    #
    # Module B6 — Dashboard Stats:
    # - GET    /api/dashboard/stats/     - Dashboard KPI summary
    path("api/dashboard/stats/", views.dashboard_stats, name="dashboard-stats"),
    path("api/", include(router.urls)),
]
