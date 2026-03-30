"""
Django Admin Configuration for Orders — Module B3

Provides admin interfaces for:
- Order: Manage orders with inline order items
- OrderItem: View order items (managed through Order admin)
"""

from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, OrderItem


# =============================================================================
# ORDER ITEM INLINE ADMIN
# =============================================================================

class OrderItemInline(TabularInline):
    """
    Inline admin for OrderItems within the Order admin.
    Displays all items in an order with read-only fields.
    """
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'unit_price', 'subtotal')
    readonly_fields = ('product', 'quantity', 'unit_price', 'subtotal')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        """Prevent adding items through admin (use API)."""
        return False


# =============================================================================
# ORDER ADMIN
# =============================================================================

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """
    Order Admin Configuration — Module B3
    
    Provides Django admin interface for managing orders.
    Features:
    - List view with key order information
    - Inline order items display
    - Status-based filtering
    - Color-coded status display
    - Search by order number and customer name
    - Read-only fields (orders managed via API)
    """
    list_display = (
        'order_number',
        'customer_name',
        'get_colored_status',
        'get_item_count',
        'total_price',
        'created_by',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name')
    fields = (
        'order_number',
        'customer_name',
        'get_colored_status',
        'total_price',
        'created_by',
        'created_at',
        'updated_at'
    )
    readonly_fields = (
        'order_number',
        'customer_name',
        'get_colored_status',
        'total_price',
        'created_by',
        'created_at',
        'updated_at'
    )
    ordering = ('-created_at',)
    list_per_page = 20
    inlines = [OrderItemInline]
    
    def get_colored_status(self, obj):
        """
        Display status with color coding for better visibility.
        """
        colors = {
            Order.STATUS_PENDING: 'orange',
            Order.STATUS_CONFIRMED: 'blue',
            Order.STATUS_SHIPPED: 'purple',
            Order.STATUS_DELIVERED: 'green',
            Order.STATUS_CANCELLED: 'red',
        }
        color = colors.get(obj.status, 'black')
        return f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>'
    get_colored_status.short_description = 'Status'
    get_colored_status.allow_tags = True
    
    def get_item_count(self, obj):
        """Display the count of items in the order."""
        return obj.items.count()
    get_item_count.short_description = 'Items'
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related and prefetch_related.
        """
        qs = super().get_queryset(request)
        return qs.select_related('created_by').prefetch_related('items')
    
    def has_add_permission(self, request):
        """Prevent creating orders through admin (use API)."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting orders through admin (use cancel API)."""
        return False


# =============================================================================
# ORDER ITEM ADMIN
# =============================================================================

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    """
    OrderItem Admin Configuration — Module B3
    
    Provides Django admin interface for viewing order items.
    All fields are read-only (items managed via Order API).
    """
    list_display = (
        'id',
        'get_order_number',
        'get_product_name',
        'quantity',
        'unit_price',
        'subtotal'
    )
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('order__order_number', 'product__name')
    fields = (
        'order',
        'product',
        'quantity',
        'unit_price',
        'subtotal'
    )
    readonly_fields = ('order', 'product', 'quantity', 'unit_price', 'subtotal')
    ordering = ('-order__created_at',)
    list_per_page = 20
    
    def get_order_number(self, obj):
        """Display order number."""
        return obj.order.order_number
    get_order_number.short_description = 'Order Number'
    
    def get_product_name(self, obj):
        """Display product name."""
        return obj.product.name
    get_product_name.short_description = 'Product'
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related.
        """
        qs = super().get_queryset(request)
        return qs.select_related('order', 'product')
    
    def has_add_permission(self, request):
        """Prevent creating order items through admin (use API)."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing order items through admin (read-only)."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting order items through admin (use cancel API)."""
        return False

