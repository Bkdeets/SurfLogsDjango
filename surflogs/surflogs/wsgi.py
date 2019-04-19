"""
WSGI config for surflogs project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.pywsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'surflogs.settings')

application = get_wsgi_application()
