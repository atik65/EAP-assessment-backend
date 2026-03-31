from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, 
    LoginView, 
    current_user_view,
    HttpOnlyLoginView,
    HttpOnlyLogoutView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', current_user_view, name='current_user'),
    # HTTP-only cookie-based authentication
    path('http-login/', HttpOnlyLoginView.as_view(), name='http_login'),
    path('http-logout/', HttpOnlyLogoutView.as_view(), name='http_logout'),
]
