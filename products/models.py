from django.db import models
from django.contrib.auth.models import User


# Example Model - Replace with your own models
class ExampleModel(models.Model):
    """
    Example model to demonstrate Django model structure.
    Replace this with your own models.
    """
    title = models.CharField(max_length=200, help_text="Title of the item")
    description = models.TextField(blank=True, help_text="Description of the item")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Example Item"
        verbose_name_plural = "Example Items"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
