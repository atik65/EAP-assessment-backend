from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ExampleModel


# Example Admin - Replace with your own admin classes
@admin.register(ExampleModel)
class ExampleModelAdmin(ModelAdmin):
    """
    Example admin class to demonstrate Django Unfold admin structure.
    Replace this with your own admin classes.
    """
    list_display = ('id', 'title', 'is_active', 'created_by', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    fields = ('title', 'description', 'created_by', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """
        Example of customizing queryset to show only user's own items for non-superusers.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        """
        Example of auto-setting created_by to current user.
        """
        if not change and not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
