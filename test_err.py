import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.test import Client
from apps.accounts.models import User

user = User.objects.filter(is_superuser=True).first()
c = Client()
c.force_login(user)

try:
    response = c.get("/dashboard/settings/rbac/", SERVER_NAME="localhost")
    print(f"Status Code: {response.status_code}")
except Exception as e:
    import traceback
    traceback.print_exc()
