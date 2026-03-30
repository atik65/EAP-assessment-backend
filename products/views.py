from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging

from .models import Category, Product, RestockQueue, check_restock_queue
from .serializers import (
    CategorySerializer,
    CategoryListSerializer,
    CategoryCreateUpdateSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    RestockQueueSerializer,
    RestockActionSerializer,
)

logger = logging.getLogger(__name__)


# =============================================================================
# CATEGORY VIEWSET
# =============================================================================

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category ViewSet — Module B2
    
    Provides full CRUD operations for product categories:
    - list: GET /api/categories/ - List all categories
    - create: POST /api/categories/ - Create a new category
    - retrieve: GET /api/categories/{id}/ - Get category details
    - partial_update: PATCH /api/categories/{id}/ - Update category name
    - destroy: DELETE /api/categories/{id}/ - Delete category (blocked if products exist)
    
    All endpoints require JWT authentication.
    """
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """
        Return different serializers for different actions.
        
        - List: CategoryListSerializer (with product count)
        - Create/Update: CategoryCreateUpdateSerializer (name only)
        - Detail: CategoryListSerializer (full info)
        """
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CategoryCreateUpdateSerializer
        else:
            return CategoryListSerializer
    
    @extend_schema(
        summary="List all categories",
        description="Get a list of all product categories with product counts",
        responses={200: CategoryListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List all categories."""
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a category",
        description="Create a new product category",
        request=CategoryCreateUpdateSerializer,
        responses={201: CategoryListSerializer}
    )
    def create(self, request, *args, **kwargs):
        """Create a new category."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return full category details using CategoryListSerializer
        category = Category.objects.get(pk=serializer.instance.pk)
        response_serializer = CategoryListSerializer(category)
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @extend_schema(
        summary="Get category details",
        description="Retrieve details of a specific category",
        responses={200: CategoryListSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Get category details."""
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update category",
        description="Update category name (partial update supported)",
        request=CategoryCreateUpdateSerializer,
        responses={200: CategoryListSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """Update category name only."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return full category details
        response_serializer = CategoryListSerializer(serializer.instance)
        return Response(response_serializer.data)
    
    @extend_schema(
        summary="Delete category",
        description="Delete a category (fails if products exist in this category)",
        responses={
            204: None,
            400: {"description": "Category has products and cannot be deleted"}
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete category with validation.
        
        Prevents deletion if any products (including archived) exist in this category.
        Returns 400 Bad Request with error message if products exist.
        """
        category = self.get_object()
        
        # Check if category has any products (including archived)
        product_count = category.products.count()
        if product_count > 0:
            return Response(
                {
                    "detail": f"Cannot delete category '{category.name}' because it has {product_count} product(s). Remove or reassign the products first."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # If no products, proceed with deletion
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Disable PUT method - only PATCH is allowed for updates
    def update(self, request, *args, **kwargs):
        """PUT method is not allowed. Use PATCH instead."""
        return Response(
            {"detail": "Method 'PUT' not allowed. Use PATCH for partial updates."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


# =============================================================================
# PRODUCT VIEWSET
# =============================================================================

class ProductViewSet(viewsets.ModelViewSet):
    """
    Product ViewSet — Module B2
    
    Provides full CRUD operations for products with automatic status management:
    - list: GET /api/products/ - List products with filters
    - create: POST /api/products/ - Create a new product
    - retrieve: GET /api/products/{id}/ - Get product details
    - partial_update: PATCH /api/products/{id}/ - Update product
    - destroy: DELETE /api/products/{id}/ - Soft-delete (archive) product
    
    Query Parameters:
    - status: Filter by status (active, out_of_stock, archived)
    - category: Filter by category UUID
    - search: Search in product name
    - ordering: Order by name, -price, -stock_quantity, etc.
    
    All endpoints require JWT authentication.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['name']
    ordering_fields = ['name', 'price', 'stock_quantity', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return products queryset.
        
        By default, excludes archived products from list view.
        Detail view can access all products including archived.
        """
        queryset = Product.objects.select_related('category', 'created_by').all()
        
        # Exclude archived products from list view by default
        if self.action == 'list':
            # Allow filtering archived products if explicitly requested
            if self.request.query_params.get('status') != Product.STATUS_ARCHIVED:
                queryset = queryset.exclude(status=Product.STATUS_ARCHIVED)
        
        return queryset
    
    def get_serializer_class(self):
        """
        Return different serializers for different actions.
        
        - List: ProductListSerializer (concise with is_low_stock)
        - Create/Update: ProductCreateUpdateSerializer (validation)
        - Detail: ProductDetailSerializer (full info)
        """
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        else:
            return ProductDetailSerializer
    
    @extend_schema(
        summary="List products",
        description="Get a list of products with filtering, searching, and ordering support",
        parameters=[
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                description='Filter by status (active, out_of_stock, archived)',
                enum=['active', 'out_of_stock', 'archived']
            ),
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.UUID,
                description='Filter by category UUID'
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                description='Search in product name'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                description='Order by: name, -price, -stock_quantity, created_at, etc.'
            ),
        ],
        responses={200: ProductListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List products with filters."""
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a product",
        description="Create a new product. Status is automatically managed based on stock quantity.",
        request=ProductCreateUpdateSerializer,
        responses={201: ProductDetailSerializer}
    )
    def create(self, request, *args, **kwargs):
        """Create a new product."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Return full product details using ProductDetailSerializer
        product = Product.objects.select_related('category', 'created_by').get(pk=serializer.instance.pk)
        response_serializer = ProductDetailSerializer(product)
        
        logger.info(f"Product created: {product.name} (ID: {product.id}) by user {request.user.email}")
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @extend_schema(
        summary="Get product details",
        description="Retrieve details of a specific product",
        responses={200: ProductDetailSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Get product details."""
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update product",
        description="Update product fields. Status is automatically managed based on stock quantity.",
        request=ProductCreateUpdateSerializer,
        responses={200: ProductDetailSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """Update product fields."""
        instance = self.get_object()
        
        # Prevent updates to archived products
        if instance.status == Product.STATUS_ARCHIVED:
            return Response(
                {"detail": "Cannot update archived products. Restore the product first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Return full product details
        product = Product.objects.select_related('category', 'created_by').get(pk=serializer.instance.pk)
        response_serializer = ProductDetailSerializer(product)
        
        logger.info(f"Product updated: {product.name} (ID: {product.id}) by user {request.user.email}")
        
        return Response(response_serializer.data)
    
    @extend_schema(
        summary="Delete (archive) product",
        description="Soft-delete a product by setting status to 'archived'. Product data is retained for order history.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Soft-delete product by archiving it.
        
        Instead of deleting the product from database, sets status to 'archived'.
        This preserves product data for order history and reporting.
        """
        product = self.get_object()
        
        # Set status to archived instead of deleting
        product.status = Product.STATUS_ARCHIVED
        product.save()
        
        logger.info(f"Product archived: {product.name} (ID: {product.id}) by user {request.user.email}")
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Disable PUT method - only PATCH is allowed for updates
    def update(self, request, *args, **kwargs):
        """PUT method is not allowed. Use PATCH instead."""
        return Response(
            {"detail": "Method 'PUT' not allowed. Use PATCH for partial updates."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


# =============================================================================
# RESTOCK QUEUE VIEWSET — MODULE B4
# =============================================================================

class RestockQueueViewSet(viewsets.ModelViewSet):
    """
    Restock Queue ViewSet — Module B4
    
    Manages the automatic restock queue for low-stock products.
    
    Endpoints:
    - list: GET /api/restock/ - List all products in restock queue
    - restock: POST /api/restock/{id}/restock/ - Add stock to a product
    - destroy: DELETE /api/restock/{id}/ - Manually remove from queue
    
    Products are automatically added when stock < min_stock_threshold
    and removed when stock >= min_stock_threshold.
    
    List is ordered by stock_quantity ASC (lowest stock first).
    """
    queryset = RestockQueue.objects.select_related('product', 'product__category').all()
    serializer_class = RestockQueueSerializer
    permission_classes = [IsAuthenticated]
    
    # Disable create and update - queue is auto-managed
    http_method_names = ['get', 'delete', 'post']  # Only allow GET, DELETE, and POST (for custom actions)
    
    @extend_schema(
        summary="List restock queue",
        description="Get all products in the restock queue, ordered by stock quantity (lowest first). "
                    "Priority is computed based on current stock levels.",
        responses={200: RestockQueueSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List all products in restock queue.
        
        Ordered by stock_quantity ASC (products with lowest stock appear first).
        """
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Get restock queue entry details",
        description="Retrieve details of a specific restock queue entry",
        responses={200: RestockQueueSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Get details of a specific restock queue entry."""
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Restock product",
        description="Add stock to a product in the restock queue. "
                    "Automatically re-evaluates queue status after restocking.",
        request=RestockActionSerializer,
        responses={200: RestockQueueSerializer}
    )
    @action(detail=True, methods=['post'])
    def restock(self, request, pk=None):
        """
        Add stock to a product and re-evaluate restock queue.
        
        Request body: {"quantity_to_add": 50}
        
        This endpoint:
        1. Validates the quantity to add
        2. Adds quantity to product's current stock
        3. Triggers restock queue re-evaluation
        4. Returns updated queue entry (or removes it if stock is now sufficient)
        """
        # Get the queue entry
        queue_entry = self.get_object()
        product = queue_entry.product
        
        # Validate input
        serializer = RestockActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quantity_to_add = serializer.validated_data['quantity_to_add']
        
        # Update stock quantity
        old_stock = product.stock_quantity
        product.stock_quantity += quantity_to_add
        product.save()  # This will automatically trigger check_restock_queue
        
        logger.info(
            f"Product restocked: {product.name} (ID: {product.id}) - "
            f"Stock: {old_stock} → {product.stock_quantity} (+{quantity_to_add}) "
            f"by user {request.user.email}"
        )
        
        # Check if product is still in queue after restock
        try:
            # Refresh from DB to get latest state
            queue_entry.refresh_from_db()
            response_serializer = RestockQueueSerializer(queue_entry)
            return Response(response_serializer.data)
        except RestockQueue.DoesNotExist:
            # Product was removed from queue (stock is now sufficient)
            return Response(
                {
                    "detail": f"Product '{product.name}' restocked successfully. "
                              f"Removed from restock queue (stock now: {product.stock_quantity}).",
                    "product": {
                        "id": str(product.id),
                        "name": product.name,
                        "stock_quantity": product.stock_quantity,
                        "min_stock_threshold": product.min_stock_threshold
                    }
                },
                status=status.HTTP_200_OK
            )
    
    @extend_schema(
        summary="Remove from queue",
        description="Manually remove a product from the restock queue. "
                    "Note: Product may be re-added automatically if stock is still low.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        """
        Manually remove a product from the restock queue.
        
        Note: If the product's stock is still below threshold, it may be
        automatically re-added to the queue on next stock change.
        """
        queue_entry = self.get_object()
        product_name = queue_entry.product.name
        
        logger.info(
            f"Product manually removed from restock queue: {product_name} "
            f"by user {request.user.email}"
        )
        
        queue_entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Disable create and update methods
    def create(self, request, *args, **kwargs):
        """Create is not allowed. Queue is automatically managed based on stock levels."""
        return Response(
            {"detail": "Cannot manually create restock queue entries. Queue is automatically managed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def update(self, request, *args, **kwargs):
        """Update is not allowed. Queue is automatically managed."""
        return Response(
            {"detail": "Cannot update restock queue entries. Queue is automatically managed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Partial update is not allowed. Queue is automatically managed."""
        return Response(
            {"detail": "Cannot update restock queue entries. Queue is automatically managed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
