from rest_framework import generics
from .models import ActivityLog
from .serializers import ActivityLogSerializer

class ActivityLogListView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    pagination_class = None

    def get_queryset(self):
        # Latest 50 entries, newest first
        return ActivityLog.objects.all()[:50]
