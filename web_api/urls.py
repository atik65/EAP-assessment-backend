from django.urls import path
from . import views

app_name = 'web_api'

# Public Web API URLs (no authentication required)
urlpatterns = [
    path('info/', views.api_info, name='api_info'),
]
