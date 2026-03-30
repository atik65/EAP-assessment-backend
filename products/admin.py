from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product


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
