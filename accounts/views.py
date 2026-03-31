from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    LoginResponseSerializer,
    UserSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Register a new user with email and password.
    Returns JWT tokens and user data.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        tokens = LoginResponseSerializer.get_tokens_for_user(user)
        
        return Response(tokens, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    POST /api/auth/login/
    Login with email and password.
    Returns JWT tokens and user data.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        tokens = LoginResponseSerializer.get_tokens_for_user(user)
        
        return Response(tokens, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    """
    GET /api/auth/me/
    Get current authenticated user profile.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class HttpOnlyLoginView(generics.GenericAPIView):
    """
    POST /api/auth/http-login/
    Login with email and password using HTTP-only cookies.
    Sets JWT tokens in secure HTTP-only cookies.
    Returns user data in response body.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return Response(
                {"detail": "Invalid email or password."},
                # status=status.HTTP_401_UNAUTHORIZED

                # login failure should not be unauthorized (401) since user is not authenticated yet, but rather a bad request (400)
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate tokens
        tokens = LoginResponseSerializer.get_tokens_for_user(user)
        
        # Create response with user data (without tokens in body)
        response_data = {
            "user": UserSerializer(user).data,
            "message": "Login successful"
        }
        response = Response(response_data, status=status.HTTP_200_OK)
        
        # Set tokens in HTTP-only cookies
        # Access token cookie (short-lived)
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,  # Prevents JavaScript access
            secure=False,    # Set to True in production with HTTPS
            samesite='Lax',  # CSRF protection
            max_age=3600,    # 1 hour (matches token lifetime)
        )
        
        # Refresh token cookie (long-lived)
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=False,    # Set to True in production with HTTPS
            samesite='Lax',
            max_age=604800,  # 7 days (matches token lifetime)
        )
        
        return response


class HttpOnlyLogoutView(generics.GenericAPIView):
    """
    GET /api/auth/http-logout/
    Logout by clearing HTTP-only cookies.
    No authentication required (cookies are cleared regardless).
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response = Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )
        
        # Clear the HTTP-only cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
