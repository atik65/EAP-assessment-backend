import uuid
from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Order(models.Model):
    """
    Order Model — Module B3
    
    Represents a customer order with automatic order number generation
    and status lifecycle management.
    
    Order Number Format: ORD-{YYYYMMDD}-{4-digit-sequence}
    Example: ORD-20250610-0023
    
    Status Lifecycle:
    - pending → confirmed | cancelled
    - confirmed → shipped | cancelled
    - shipped → delivered
    - delivered → (terminal)
    - cancelled → (terminal)
    """
    
    # Status choices for order lifecycle
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    
    # Valid status transitions
    STATUS_TRANSITIONS = {
        STATUS_PENDING: [STATUS_CONFIRMED, STATUS_CANCELLED],
        STATUS_CONFIRMED: [STATUS_SHIPPED, STATUS_CANCELLED],
        STATUS_SHIPPED: [STATUS_DELIVERED],
        STATUS_DELIVERED: [],  # Terminal state
        STATUS_CANCELLED: [],  # Terminal state
    }
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the order"
    )
    order_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Auto-generated order number (ORD-YYYYMMDD-####)"
    )
    customer_name = models.CharField(
        max_length=200,
        help_text="Name of the customer placing the order"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        help_text="Current status of the order"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total price of the order (computed from items)"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        help_text="User who created this order"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when order was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when order was last updated"
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['order_number']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.order_number} - {self.customer_name} ({self.status})"
    
    @classmethod
    def generate_order_number(cls):
        """
        Generate a unique order number in the format: ORD-{YYYYMMDD}-{####}
        
        The sequence number resets daily and is zero-padded to 4 digits.
        
        Returns:
            str: Unique order number (e.g., "ORD-20250610-0023")
        """
        today = date.today()
        date_str = today.strftime('%Y%m%d')
        prefix = f"ORD-{date_str}-"
        
        # Get the count of orders created today
        today_orders = cls.objects.filter(
            order_number__startswith=prefix
        ).count()
        
        # Increment sequence number (1-based)
        sequence = today_orders + 1
        
        # Format with zero-padding
        order_number = f"{prefix}{sequence:04d}"
        
        return order_number
    
    def can_transition_to(self, new_status):
        """
        Check if the order can transition to a new status.
        
        Args:
            new_status (str): The target status to transition to
            
        Returns:
            bool: True if transition is allowed, False otherwise
        """
        allowed_statuses = self.STATUS_TRANSITIONS.get(self.status, [])
        return new_status in allowed_statuses
    
    def compute_total_price(self):
        """
        Compute the total price of the order from all order items.
        
        Returns:
            Decimal: Sum of all item subtotals
        """
        total = sum(
            item.subtotal for item in self.items.all()
        )
        return Decimal(str(total))


class OrderItem(models.Model):
    """
    Order Item Model — Module B3
    
    Represents a single line item in an order.
    Captures product details at the time of order (price snapshot).
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the order item"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The order this item belongs to"
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        help_text="The product being ordered"
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Quantity of the product ordered (minimum 1)"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Price per unit at the time of order (snapshot)"
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Subtotal for this item (quantity × unit_price)"
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ['id']
        # Prevent duplicate products in the same order
        unique_together = [['order', 'product']]

    def __str__(self):
        return f"{self.product.name} × {self.quantity} @ {self.unit_price}"
    
    def save(self, *args, **kwargs):
        """
        Override save to automatically compute subtotal.
        
        Subtotal = quantity × unit_price
        """
        self.subtotal = Decimal(str(self.quantity)) * self.unit_price
        super().save(*args, **kwargs)
