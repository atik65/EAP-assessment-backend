"""
Serializers for Order and OrderItem models — Module B3

This module provides serializers for order management with:
- Order creation with multiple items in a single atomic transaction
- Stock validation and deduction
- Automatic order number generation
- Status transition validation
- Order cancellation with stock restoration
"""

from rest_framework import serializers
from django.db import transaction
from decimal import Decimal

from .models import Order, OrderItem
from products.models import Product


# ============================================================================
# Order Item Serializers
# ============================================================================

class OrderItemProductSerializer(serializers.ModelSerializer):
    """
    Nested serializer for product information in order items.
    Used for read operations to show product details.
    """
    class Meta:
        model = Product
        fields = ['id', 'name']
        read_only_fields = fields


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem with nested product information.
    Used in order detail responses.
    """
    product = OrderItemProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'quantity',
            'unit_price',
            'subtotal'
        ]
        read_only_fields = fields


class OrderItemCreateSerializer(serializers.Serializer):
    """
    Serializer for creating order items.
    Used in the order creation request payload.
    """
    product_id = serializers.UUIDField(
        help_text="UUID of the product to order"
    )
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="Quantity to order (minimum 1)"
    )
    
    def validate_product_id(self, value):
        """Validate that the product exists."""
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                f"Product with ID '{value}' does not exist."
            )
        return value


# ============================================================================
# Order Serializers
# ============================================================================

class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing orders.
    Includes computed item_count field.
    """
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_name',
            'status',
            'total_price',
            'item_count',
            'created_at'
        ]
        read_only_fields = fields
    
    def get_item_count(self, obj):
        """Get the number of items in the order."""
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for order detail view.
    Includes all order items with nested product information.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_name',
            'status',
            'total_price',
            'created_at',
            'updated_at',
            'items'
        ]
        read_only_fields = fields


class OrderCreateSerializer(serializers.Serializer):
    """
    Serializer for creating orders with multiple items.
    
    Handles:
    - Validation of duplicate products
    - Stock availability checks
    - Atomic order + items creation
    - Automatic stock deduction
    - Order number generation
    - Restock queue updates
    """
    customer_name = serializers.CharField(
        max_length=200,
        help_text="Name of the customer placing the order"
    )
    items = OrderItemCreateSerializer(
        many=True,
        help_text="List of order items"
    )
    
    def validate_items(self, value):
        """
        Validate that:
        1. At least one item is provided
        2. No duplicate products in the order
        """
        if not value:
            raise serializers.ValidationError(
                "At least one item is required."
            )
        
        # Check for duplicate products
        product_ids = [item['product_id'] for item in value]
        if len(product_ids) != len(set(product_ids)):
            # Find the duplicate product
            seen = set()
            for product_id in product_ids:
                if product_id in seen:
                    try:
                        product = Product.objects.get(id=product_id)
                        raise serializers.ValidationError(
                            f"Product '{product.name}' is already added to this order."
                        )
                    except Product.DoesNotExist:
                        pass
                seen.add(product_id)
        
        return value
    
    def validate(self, data):
        """
        Validate stock availability and product status for all items.
        
        Checks:
        1. All products have status = 'active'
        2. Sufficient stock quantity for each item
        """
        items = data['items']
        
        for item_data in items:
            product_id = item_data['product_id']
            requested_quantity = item_data['quantity']
            
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({
                    'items': f"Product with ID '{product_id}' does not exist."
                })
            
            # Check if product is active
            if product.status != Product.STATUS_ACTIVE:
                raise serializers.ValidationError({
                    'items': f"Product '{product.name}' is currently unavailable."
                })
            
            # Check stock availability
            if product.stock_quantity < requested_quantity:
                available = product.stock_quantity
                raise serializers.ValidationError({
                    'items': f"Only {available} item(s) available for '{product.name}'."
                })
        
        return data
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Create order with items in an atomic transaction.
        
        Steps:
        1. Generate order number
        2. Create order
        3. Create order items
        4. Deduct stock quantity
        5. Snapshot unit prices
        6. Compute total price
        7. Trigger restock queue check
        
        Returns:
            Order: The created order instance
        """
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Generate unique order number
        order_number = Order.generate_order_number()
        
        # Create order
        order = Order.objects.create(
            order_number=order_number,
            customer_name=validated_data['customer_name'],
            status=Order.STATUS_PENDING,
            created_by=user,
            total_price=Decimal('0.00')
        )
        
        # Create order items and deduct stock
        total_price = Decimal('0.00')
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            quantity = item_data['quantity']
            
            # Snapshot the current price
            unit_price = product.price
            
            # Create order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price
                # subtotal is computed automatically in model save()
            )
            
            # Deduct stock (this triggers Product.save() and restock queue check)
            product.stock_quantity -= quantity
            product.save()
            
            # Add to total price
            total_price += unit_price * Decimal(str(quantity))
        
        # Update order total price
        order.total_price = total_price
        order.save()
        
        return order


class OrderStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating order status.
    Validates status transitions according to the lifecycle rules.
    """
    status = serializers.ChoiceField(
        choices=Order.STATUS_CHOICES,
        help_text="New status for the order"
    )
    
    def validate_status(self, value):
        """
        Validate that the status transition is allowed.
        
        Transition rules:
        - pending → confirmed | cancelled
        - confirmed → shipped | cancelled
        - shipped → delivered
        - delivered → (terminal, no changes allowed)
        - cancelled → (terminal, no changes allowed)
        """
        order = self.instance
        
        if not order.can_transition_to(value):
            raise serializers.ValidationError(
                f"Cannot transition from '{order.status}' to '{value}'. "
                f"Invalid status transition."
            )
        
        return value
    
    def update(self, instance, validated_data):
        """Update the order status."""
        instance.status = validated_data['status']
        instance.save()
        return instance
