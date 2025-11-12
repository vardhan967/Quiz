"""
WSGI config for Quiz_Base project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Quiz_Base.settings')

application = get_wsgi_application()

# If WhiteNoise is installed, wrap the application so static files can be served
# directly by the WSGI app (helpful for simple deployments using Gunicorn).
try:
	from whitenoise import WhiteNoise
	BASE_DIR = Path(__file__).resolve().parent.parent
	static_root = os.path.join(BASE_DIR, 'staticfiles')
	application = WhiteNoise(application, root=static_root)
except Exception:
	# WhiteNoise isn't available or failed to initialize — that's fine; static
	# assets should be served by the webserver or storage in production.
	pass
