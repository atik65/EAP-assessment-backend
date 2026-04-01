from rest_framework import serializers
from .models import ActivityLog
from accounts.serializers import UserSerializer

class ActivityLogSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.ReadOnlyField(source='performed_by.username')
    
    class ModelSerializer:
        model = ActivityLog

    class Meta:
        model = ActivityLog
        fields = [
            'id',
            'action',
            'performed_by',
            'performed_by_name',
            'timestamp',
            'entity_type',
            'entity_id'
        ]
        read_only_fields = fields
