from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'performed_by', 'timestamp', 'entity_type')
    list_filter = ('entity_type', 'timestamp', 'performed_by')
    search_fields = ('action', 'entity_id')
    readonly_fields = ('id', 'action', 'performed_by', 'timestamp', 'entity_type', 'entity_id')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
