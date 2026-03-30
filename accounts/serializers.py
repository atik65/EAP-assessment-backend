from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        # validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'},
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'role']
        extra_kwargs = {
            'username': {'required': False},  # Auto-generate if not provided
        }

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def validate_email(self, value):
        """Validate email uniqueness."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """Create and return a new user with encrypted password."""
        validated_data.pop('password2')
        
        # Auto-generate username from email if not provided
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email'].split('@')[0]
        
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True, 
        write_only=True,
        style={'input_type': 'password'}
    )


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer for login response with tokens and user data.
    """
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    
    @staticmethod
    def get_tokens_for_user(user):
        """Generate JWT tokens for a user."""
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }
