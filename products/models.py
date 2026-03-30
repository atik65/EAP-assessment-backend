import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


class Category(models.Model):
    """
    Product Category Model
    
    Represents a category for organizing products in the inventory system.
    Categories are used to group related products together.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the category"
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Name of the category (must be unique)"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories',
        help_text="User who created this category"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when category was created"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product Model with Automatic Status Management
    
    Represents a product in the inventory system with automatic status updates:
    - When stock_quantity reaches 0, status automatically changes to 'out_of_stock'
    - When stock is replenished (> 0) and status is 'out_of_stock', it changes to 'active'
    """
    
    # Status choices for product availability
    STATUS_ACTIVE = 'active'
    STATUS_OUT_OF_STOCK = 'out_of_stock'
    STATUS_ARCHIVED = 'archived'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_OUT_OF_STOCK, 'Out of Stock'),
        (STATUS_ARCHIVED, 'Archived'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the product"
    )
    name = models.CharField(
        max_length=200,
        help_text="Name of the product"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        help_text="Product category"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Price of the product (must be non-negative)"
    )
    stock_quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Current stock quantity (must be non-negative)"
    )
    min_stock_threshold = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Minimum stock threshold for restock alerts"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        help_text="Product status (automatically managed based on stock)"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        help_text="User who created this product"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when product was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when product was last updated"
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['stock_quantity']),
        ]

    def __str__(self):
        return f"{self.name} (Stock: {self.stock_quantity})"
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically manage product status based on stock quantity.
        
        Rules:
        - If stock_quantity == 0 → status = 'out_of_stock'
        - If stock_quantity > 0 and status == 'out_of_stock' → status = 'active'
        - Archived products remain archived regardless of stock
        
        Also triggers restock queue check after save (Module B4).
        """
        # Only auto-manage status if not archived
        if self.status != self.STATUS_ARCHIVED:
            if self.stock_quantity == 0:
                self.status = self.STATUS_OUT_OF_STOCK
            elif self.stock_quantity > 0 and self.status == self.STATUS_OUT_OF_STOCK:
                self.status = self.STATUS_ACTIVE
        
        super().save(*args, **kwargs)
        
        # Trigger restock queue check after save (Module B4)
        check_restock_queue(self)
    
    @property
    def is_low_stock(self):
        """
        Check if product stock is below the minimum threshold.
        
        Returns:
            bool: True if stock_quantity < min_stock_threshold, False otherwise
        """
        return self.stock_quantity < self.min_stock_threshold


class RestockQueue(models.Model):
    """
    Restock Queue Model — Module B4
    
    Automatically manages a priority queue of products that need restocking.
    Products are added when stock falls below minimum threshold and removed
    when stock is replenished above threshold.
    
    Priority is computed dynamically based on current stock levels:
    - High: stock_quantity == 0 (out of stock)
    - Medium: stock_quantity <= min_stock_threshold / 2
    - Low: stock_quantity < min_stock_threshold (but above half)
    """
    
    # Priority levels (computed, not stored)
    PRIORITY_HIGH = 'High'
    PRIORITY_MEDIUM = 'Medium'
    PRIORITY_LOW = 'Low'
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the restock queue entry"
    )
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='restock_queue_entry',
        help_text="Product that needs restocking"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when product was added to queue"
    )
    
    class Meta:
        verbose_name = "Restock Queue Entry"
        verbose_name_plural = "Restock Queue"
        ordering = ['product__stock_quantity', 'added_at']  # Lowest stock first, then oldest
    
    def __str__(self):
        return f"{self.product.name} - {self.priority} Priority"
    
    @property
    def priority(self):
        """
        Compute priority level based on current stock quantity.
        
        Priority Logic:
        - High: stock_quantity == 0 (completely out of stock)
        - Medium: 1 <= stock_quantity <= floor(min_stock_threshold / 2)
        - Low: stock above half threshold but still below minimum
        
        Returns:
            str: Priority level ('High', 'Medium', or 'Low')
        """
        stock = self.product.stock_quantity
        threshold = self.product.min_stock_threshold
        
        if stock == 0:
            return self.PRIORITY_HIGH
        elif stock <= threshold // 2:  # floor division
            return self.PRIORITY_MEDIUM
        else:
            return self.PRIORITY_LOW


# =============================================================================
# RESTOCK QUEUE MANAGEMENT HELPER
# =============================================================================

def check_restock_queue(product):
    """
    Auto-manage restock queue for a product based on stock levels.
    
    This function should be called after any stock quantity change (orders, manual restock, etc.)
    
    Logic:
    - If stock < min_stock_threshold AND not in queue → ADD to queue
    - If stock >= min_stock_threshold AND in queue → REMOVE from queue
    
    Args:
        product (Product): The product to check for restock queue management
    
    Returns:
        tuple: (action_taken, queue_entry or None)
            - action_taken: 'added', 'removed', or 'no_change'
            - queue_entry: RestockQueue instance if added, None otherwise
    """
    # Skip archived products
    if product.status == Product.STATUS_ARCHIVED:
        # Remove from queue if it exists
        try:
            entry = RestockQueue.objects.get(product=product)
            entry.delete()
            return ('removed', None)
        except RestockQueue.DoesNotExist:
            return ('no_change', None)
    
    # Check if product should be in queue
    should_be_in_queue = product.stock_quantity < product.min_stock_threshold
    
    try:
        # Check if product is already in queue
        queue_entry = RestockQueue.objects.get(product=product)
        
        if not should_be_in_queue:
            # Remove from queue - stock is now sufficient
            queue_entry.delete()
            return ('removed', None)
        else:
            # Already in queue and should stay - no change
            return ('no_change', queue_entry)
    
    except RestockQueue.DoesNotExist:
        # Product not in queue
        if should_be_in_queue:
            # Add to queue - stock is below threshold
            queue_entry = RestockQueue.objects.create(product=product)
            return ('added', queue_entry)
        else:
            # Not in queue and shouldn't be - no change
            return ('no_change', None)
