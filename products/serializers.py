from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ExampleModel


# Example Serializer - Replace with your own serializers
class ExampleModelSerializer(serializers.ModelSerializer):
    """
    Example serializer to demonstrate Django REST Framework serializer structure.
    Replace this with your own serializers.
    """
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = ExampleModel
        fields = ['id', 'title', 'description', 'created_by', 'created_by_username', 
                  'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


# Example of a custom serializer with SerializerMethodField
class ExampleDetailSerializer(serializers.ModelSerializer):
    """
    Example detail serializer with custom fields and methods.
    """
    custom_field = serializers.SerializerMethodField()
    
    class Meta:
        model = ExampleModel
        fields = '__all__'
    
    def get_custom_field(self, obj):
        """
        Example method to compute a custom field value.
        """
        return f"{obj.title} - {obj.id}"


# Example of a write-only serializer for create/update operations
class ExampleCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Example serializer for create and update operations.
    """
    class Meta:
        model = ExampleModel
        fields = ['title', 'description', 'is_active']
    
    def create(self, validated_data):
        # Add custom logic before creating
        if 'created_by' not in validated_data and self.context.get('request'):
            validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

