from rest_framework import serializers
from django.contrib.auth.models import User

# Add your admin API serializers here
# Example:
# from products.models import ExampleModel
#
# class AdminExampleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ExampleModel
#         fields = '__all__'  # Admin can see all fields


# Example User serializer for admin operations
class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined']
        read_only_fields = ['id', 'date_joined']
