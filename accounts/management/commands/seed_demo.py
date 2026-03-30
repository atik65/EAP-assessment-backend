from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a demo user for testing (demo@demo.com / demo1234) with manager role'

    def handle(self, *args, **kwargs):
        """
        Create or update demo user.
        Idempotent - safe to run multiple times.
        """
        email = 'demo@demo.com'
        password = 'demo1234'
        username = 'demo'
        role = 'manager'
        
        # Check if user already exists
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'role': role,
                'is_active': True,
            }
        )
        
        if created:
            # Set password for new user
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Demo user created successfully: {email} / {password}'
                )
            )
        else:
            # Update password for existing user (in case it was changed)
            user.set_password(password)
            user.role = role
            user.is_active = True
            user.save()
            self.stdout.write(
                self.style.WARNING(
                    f'⚠ Demo user already exists. Password reset to: {password}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📧 Email: {email}\n🔑 Password: {password}\n👤 Role: {role}\n'
            )
        )
