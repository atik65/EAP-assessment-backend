import uuid
from django.db import models
from django.conf import settings

class ActivityLog(models.Model):
    ENTITY_TYPE_CHOICES = [
        ('order', 'Order'),
        ('product', 'Product'),
        ('restock', 'Restock'),
        ('auth', 'Auth'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=500)
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_logs'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPE_CHOICES)
    entity_id = models.UUIDField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.action} at {self.timestamp}"

    @classmethod
    def log(cls, action, user=None, entity_type=None, entity_id=None):
        """
        Logging Convention: ActivityLog.log(action, user, entity_type, entity_id)
        """
        return cls.objects.create(
            action=action,
            performed_by=user,
            entity_type=entity_type,
            entity_id=entity_id
        )
