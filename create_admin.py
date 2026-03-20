import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secure_library.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def create_admin():
    email = 'admin@library.com'
    password = 'Admin@123'
    username = 'admin'

    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ Admin created: {email} | {password}")
        
        # Ensure user profile exists
        UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': 'ADMIN', 'phone': '9999999999'}
        )
    else:
        print("✅ Admin already exists.")

if __name__ == '__main__':
    create_admin()
