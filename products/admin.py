from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product, RestockQueue


# =============================================================================
# CATEGORY ADMIN
# =============================================================================

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Category Admin Configuration — Module B2
    
    Provides Django admin interface for managing product categories.
    Features:
    - List view with product count
    - Search by category name
    - Filter by creation date
    - Auto-set created_by to current user
    """
    list_display = ('id', 'name', 'get_product_count', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    fields = ('name', 'created_by', 'created_at')
    readonly_fields = ('id', 'created_by', 'created_at')
    ordering = ('name',)
    
    def get_product_count(self, obj):
        """
        Display the count of products in this category (excluding archived).
        """
        count = obj.products.exclude(status=Product.STATUS_ARCHIVED).count()
        return count
    get_product_count.short_description = 'Products'
    
    def get_queryset(self, request):
        """
        Optimize queryset with prefetch for product counts.
        """
        qs = super().get_queryset(request)
        return qs.select_related('created_by')
    
    def save_model(self, request, obj, form, change):
        """
        Auto-set created_by to current user on creation.
        """
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# =============================================================================
# PRODUCT ADMIN
# =============================================================================

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Product Admin Configuration — Module B2
    
    Provides Django admin interface for managing products.
    Features:
    - List view with key information and low stock indicator
    - Filters by status, category, and stock levels
    - Search by product name
    - Color-coded status display
    - Auto-set created_by to current user
    - Status is automatically managed by model save()
    """
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'stock_quantity',
        'min_stock_threshold',
        'get_colored_status',
        'get_low_stock_indicator',
        'created_at'
    )
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('name', 'category__name')
    fields = (
        'name',
        'category',
        'price',
        'stock_quantity',
        'min_stock_threshold',
        'status',
        'created_by',
        'created_at',
        'updated_at'
    )
    readonly_fields = ('id', 'status', 'created_by', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 20
    
    def get_colored_status(self, obj):
        """
        Display status with color coding for better visibility.
        """
        colors = {
            Product.STATUS_ACTIVE: 'green',
            Product.STATUS_OUT_OF_STOCK: 'red',
            Product.STATUS_ARCHIVED: 'gray'
        }
        color = colors.get(obj.status, 'black')
        return f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>'
    get_colored_status.short_description = 'Status'
    get_colored_status.allow_tags = True
    
    def get_low_stock_indicator(self, obj):
        """
        Display a visual indicator if product is low on stock.
        """
        if obj.status == Product.STATUS_ARCHIVED:
            return '📦 Archived'
        elif obj.stock_quantity == 0:
            return '🔴 Out of Stock'
        elif obj.is_low_stock:
            return '⚠️ Low Stock'
        else:
            return '✅ OK'
    get_low_stock_indicator.short_description = 'Stock Status'
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related for better performance.
        """
        qs = super().get_queryset(request)
        return qs.select_related('category', 'created_by')
    
    def save_model(self, request, obj, form, change):
        """
        Auto-set created_by to current user on creation.
        Status is automatically managed by Product.save() method.
        """
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# =============================================================================
# RESTOCK QUEUE ADMIN — MODULE B4
# =============================================================================

@admin.register(RestockQueue)
class RestockQueueAdmin(ModelAdmin):
    """
    Restock Queue Admin Configuration — Module B4
    
    Provides Django admin interface for viewing and managing the restock queue.
    Features:
    - List view with product details and priority
    - Priority-based color coding
    - Read-only display (queue is auto-managed)
    - Ordered by stock quantity (lowest first)
    """
    list_display = (
        'id',
        'get_product_name',
        'get_stock_quantity',
        'get_min_threshold',
        'get_colored_priority',
        'added_at'
    )
    list_filter = ('added_at',)
    search_fields = ('product__name',)
    fields = (
        'product',
        'get_product_details',
        'get_priority_level',
        'added_at'
    )
    readonly_fields = ('product', 'get_product_details', 'get_priority_level', 'added_at')
    ordering = ('product__stock_quantity', 'added_at')
    list_per_page = 20
    
    def get_product_name(self, obj):
        """Display product name."""
        return obj.product.name
    get_product_name.short_description = 'Product'
    
    def get_stock_quantity(self, obj):
        """Display current stock quantity."""
        return obj.product.stock_quantity
    get_stock_quantity.short_description = 'Current Stock'
    
    def get_min_threshold(self, obj):
        """Display minimum stock threshold."""
        return obj.product.min_stock_threshold
    get_min_threshold.short_description = 'Min Threshold'
    
    def get_colored_priority(self, obj):
        """
        Display priority with color coding for better visibility.
        """
        priority = obj.priority
        colors = {
            RestockQueue.PRIORITY_HIGH: 'red',
            RestockQueue.PRIORITY_MEDIUM: 'orange',
            RestockQueue.PRIORITY_LOW: 'blue'
        }
        color = colors.get(priority, 'black')
        
        # Add emoji for visual distinction
        emojis = {
            RestockQueue.PRIORITY_HIGH: '🔴',
            RestockQueue.PRIORITY_MEDIUM: '🟠',
            RestockQueue.PRIORITY_LOW: '🔵'
        }
        emoji = emojis.get(priority, '')
        
        return f'<span style="color: {color}; font-weight: bold;">{emoji} {priority}</span>'
    get_colored_priority.short_description = 'Priority'
    get_colored_priority.allow_tags = True
    
    def get_product_details(self, obj):
        """
        Display detailed product information in the detail view.
        """
        product = obj.product
        return (
            f"Name: {product.name}\n"
            f"Stock: {product.stock_quantity} / {product.min_stock_threshold} (threshold)\n"
            f"Status: {product.get_status_display()}\n"
            f"Category: {product.category.name}"
        )
    get_product_details.short_description = 'Product Details'
    
    def get_priority_level(self, obj):
        """Display priority level in detail view."""
        return obj.priority
    get_priority_level.short_description = 'Priority Level'
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related for better performance.
        """
        qs = super().get_queryset(request)
        return qs.select_related('product', 'product__category')
    
    def has_add_permission(self, request):
        """
        Disable manual creation - queue is automatically managed.
        """
        return False
    
    def has_change_permission(self, request, obj=None):
        """
        Disable editing - queue is automatically managed.
        Allow viewing only.
        """
        return False
    
    def has_delete_permission(self, request, obj=None):
        """
        Allow manual deletion (removal from queue).
        """
        return True
