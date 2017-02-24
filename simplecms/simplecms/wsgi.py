"""
WSGI config for simplecms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from simplecms import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simplecms.settings")

if settings.DEBUG==True:
    application = get_wsgi_application()
else:    # Running on Heroku
    from dj_static import Cling  
    application = Cling(get_wsgi_application())

