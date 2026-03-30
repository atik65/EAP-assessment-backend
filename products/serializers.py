from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Product

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
        fields = ['id', 'name']
        read_only_fields = ['id']


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category List Serializer
    
    Used for listing categories with full information including creation details.
    """
    created_by_email = serializers.EmailField(
        source='created_by.email',
        read_only=True,
        allow_null=True
    )
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_by', 'created_by_email', 'product_count', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']
    
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
        fields = ['name']
    
    def create(self, validated_data):
        """
        Create a new category and auto-set created_by from request context.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
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
            'id',
            'name',
            'category',
            'price',
            'stock_quantity',
            'min_stock_threshold',
            'status',
            'is_low_stock',
            'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']
    
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
        source='created_by.email',
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'price',
            'stock_quantity',
            'min_stock_threshold',
            'status',
            'is_low_stock',
            'created_by',
            'created_by_email',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_by', 'created_at', 'updated_at']
    
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
        fields = [
            'name',
            'category',
            'price',
            'stock_quantity',
            'min_stock_threshold'
        ]
    
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
            raise serializers.ValidationError("Minimum stock threshold must be non-negative.")
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
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Update a product.
        Status is automatically managed by the model's save() method.
        """
        return super().update(instance, validated_data)

