from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'examples', views.ExampleModelViewSet, basename='example')

# The API URLs are determined automatically by the router
urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # JWT Authentication endpoints
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Custom API endpoints
    path('api/health/', views.health_check, name='health_check'),
    path('api/statistics/', views.get_statistics, name='get_statistics'),
]

