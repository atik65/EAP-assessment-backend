from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Product, RestockQueue

User = get_user_model()


# =============================================================================
# CATEGORY SERIALIZERS
# =============================================================================


class CategorySerializer(serializers.ModelSerializer):
    """
    Simple Category Serializer

    Used for nested representation in product serializers and category detail view.
    Displays only id and name for clean nested objects.
    """

    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category List Serializer

    Used for listing categories with full information including creation details.
    """

    created_by_email = serializers.EmailField(
        source="created_by.email", read_only=True, allow_null=True
    )
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "created_by",
            "created_by_email",
            "product_count",
            "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_product_count(self, obj):
        """
        Get the count of products in this category (excluding archived products).
        """
        return obj.products.exclude(status=Product.STATUS_ARCHIVED).count()


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Category Create/Update Serializer

    Used for creating and updating categories.
    Only allows modification of the name field.
    """

    class Meta:
        model = Category
        fields = ["name"]

    def create(self, validated_data):
        """
        Create a new category and auto-set created_by from request context.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
        return super().create(validated_data)


# =============================================================================
# PRODUCT SERIALIZERS
# =============================================================================


class ProductListSerializer(serializers.ModelSerializer):
    """
    Product List Serializer

    Used for product listing with nested category information and computed fields.
    Includes the is_low_stock field to indicate products below minimum threshold.
    """

    category = CategorySerializer(read_only=True)
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "stock_quantity",
            "min_stock_threshold",
            "status",
            "is_low_stock",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def get_is_low_stock(self, obj):
        """
        Check if product stock is below the minimum threshold.

        Returns:
            bool: True if stock_quantity < min_stock_threshold
        """
        return obj.is_low_stock


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Product Detail Serializer

    Comprehensive serializer for product detail view with all information
    including nested category and user details.
    """

    category = CategorySerializer(read_only=True)
    is_low_stock = serializers.SerializerMethodField()
    created_by_email = serializers.EmailField(
        source="created_by.email", read_only=True, allow_null=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "stock_quantity",
            "min_stock_threshold",
            "status",
            "is_low_stock",
            "created_by",
            "created_by_email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_by", "created_at", "updated_at"]

    def get_is_low_stock(self, obj):
        """
        Check if product stock is below the minimum threshold.

        Returns:
            bool: True if stock_quantity < min_stock_threshold
        """
        return obj.is_low_stock


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Product Create/Update Serializer

    Used for creating and updating products.
    Validates all input fields and auto-manages status based on stock quantity.
    """

    class Meta:
        model = Product
        fields = ["name", "category", "price", "stock_quantity", "min_stock_threshold"]

    def validate_price(self, value):
        """
        Validate that price is non-negative.
        """
        if value < 0:
            raise serializers.ValidationError("Price must be non-negative.")
        return value

    def validate_stock_quantity(self, value):
        """
        Validate that stock quantity is non-negative.
        """
        if value < 0:
            raise serializers.ValidationError("Stock quantity must be non-negative.")
        return value

    def validate_min_stock_threshold(self, value):
        """
        Validate that minimum stock threshold is non-negative.
        """
        if value < 0:
            raise serializers.ValidationError(
                "Minimum stock threshold must be non-negative."
            )
        return value

    def validate_category(self, value):
        """
        Validate that the category exists and is accessible.
        """
        if not value:
            raise serializers.ValidationError("Category is required.")
        return value

    def create(self, validated_data):
        """
        Create a new product and auto-set created_by from request context.
        Status is automatically managed by the model's save() method.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update a product.
        Status is automatically managed by the model's save() method.
        """
        return super().update(instance, validated_data)


# =============================================================================
# RESTOCK QUEUE SERIALIZERS — MODULE B4
# =============================================================================


class RestockQueueProductSerializer(serializers.ModelSerializer):
    """
    Simplified Product Serializer for Restock Queue

    Shows essential product information for restock queue entries.
    """

    class Meta:
        model = Product
        fields = ["id", "name", "stock_quantity", "min_stock_threshold"]
        read_only_fields = ["id", "name", "stock_quantity", "min_stock_threshold"]


class RestockQueueSerializer(serializers.ModelSerializer):
    """
    Restock Queue List Serializer — Module B4

    Displays restock queue entries with nested product information and computed priority.
    Priority is dynamically calculated based on current stock levels.
    """

    product = RestockQueueProductSerializer(read_only=True)
    priority = serializers.SerializerMethodField()

    class Meta:
        model = RestockQueue
        fields = ["id", "product", "priority", "added_at"]
        read_only_fields = ["id", "product", "added_at"]

    def get_priority(self, obj):
        """
        Get the computed priority level from the model property.

        Returns:
            str: Priority level ('High', 'Medium', or 'Low')
        """
        return obj.priority


class RestockActionSerializer(serializers.Serializer):
    """
    Restock Action Serializer — Module B4

    Used for manual restocking of products.
    Validates the quantity to add and performs the stock update.
    """

    quantity_to_add = serializers.IntegerField(
        min_value=1, help_text="Quantity to add to current stock (must be positive)"
    )

    def validate_quantity_to_add(self, value):
        """
        Validate that quantity to add is positive.
        """
        if value < 1:
            raise serializers.ValidationError("Quantity to add must be at least 1.")
        return value


# =============================================================================
# DASHBOARD STATS SERIALIZERS — MODULE B6
# =============================================================================


class ProductSummarySerializer(serializers.ModelSerializer):
    """
    Product Summary Serializer for Dashboard — Module B6

    Displays product information with derived status field.
    """

    status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "stock_quantity", "status"]
        read_only_fields = ["id", "name", "stock_quantity"]

    def get_status(self, obj):
        """
        Derive status based on stock levels:
        - 'out_of_stock': stock_quantity == 0
        - 'low_stock': stock_quantity < min_stock_threshold (but > 0)
        - 'ok': stock_quantity >= min_stock_threshold

        Returns:
            str: Status ('out_of_stock', 'low_stock', or 'ok')
        """
        if obj.stock_quantity == 0:
            return "out_of_stock"
        elif obj.stock_quantity < obj.min_stock_threshold:
            return "low_stock"
        else:
            return "ok"


class DashboardStatsSerializer(serializers.Serializer):
    """
    Dashboard Stats Serializer — Module B6

    Aggregation serializer for dashboard KPI cards.
    Returns comprehensive statistics including orders, revenue, and inventory status.
    """

    orders_today = serializers.IntegerField(
        help_text="Count of all orders created today"
    )
    pending_orders = serializers.IntegerField(
        help_text="Count of orders with status = pending"
    )
    completed_orders = serializers.IntegerField(
        help_text="Count of delivered orders created today"
    )
    revenue_today = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Sum of total_price for non-cancelled orders created today",
    )
    low_stock_count = serializers.IntegerField(
        help_text="Count of products where stock_quantity < min_stock_threshold"
    )
    product_summary = ProductSummarySerializer(
        many=True,
        help_text="All products with derived status (low_stock/out_of_stock/ok)",
    )
