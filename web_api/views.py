from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


# Example public API view (no authentication required)
@extend_schema(
    tags=['Public API'],
    summary="Public API Info",
    description="Get information about the public API",
)
@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    """Public API information endpoint"""
    return Response({
        'name': 'Public Web API',
        'version': '1.0.0',
        'description': 'Public API endpoints - no authentication required',
        'note': 'Add your public API views here'
    })

