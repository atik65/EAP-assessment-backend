from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


# Example admin API view (authentication required)
@extend_schema(
    tags=['Admin API'],
    summary="Admin API Info",
    description="Get information about the admin API (requires authentication)",
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_api_info(request):
    """Admin API information endpoint"""
    return Response({
        'name': 'Admin API',
        'version': '1.0.0',
        'description': 'Admin API endpoints - authentication required',
        'user': request.user.username,
        'note': 'Add your admin API views here'
    })


# Example admin-only endpoint
@extend_schema(
    tags=['Admin API'],
    summary="Admin Dashboard Stats",
    description="Get dashboard statistics (admin only)",
)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    """Admin dashboard statistics"""
    return Response({
        'message': 'Admin dashboard endpoint',
        'note': 'Add your statistics here'
    })
