"""
WSGI config for studio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Production by default. WSGI/ASGI are what a real server loads, and the generated
# default was dev -- DEBUG on, any host, and the SECRET_KEY committed in git.
# Production refuses to start without DJANGO_SECRET_KEY, so a missing variable
# fails loudly instead of quietly serving a debug site. manage.py stays on dev.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studio.settings.production")

application = get_wsgi_application()
