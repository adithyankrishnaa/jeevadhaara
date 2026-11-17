"""
ASGI config for jeevadhaara project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jeevadhaara.settings')

application = get_asgi_application()
