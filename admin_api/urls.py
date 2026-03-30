from django.urls import path
from . import views

app_name = 'admin_api'

# Admin API URLs (authentication required)
urlpatterns = [
    path('info/', views.admin_api_info, name='api_info'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
]
