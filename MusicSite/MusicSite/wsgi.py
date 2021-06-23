"""
WSGI config for music project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicSite.settings')
os.environ['APP_TOKEN'] = 'AgAAAAAVXvrzAAZUx8r6G2rp3EZGpwXtTZI4KNg'

application = get_wsgi_application()
