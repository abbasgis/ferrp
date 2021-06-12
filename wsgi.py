"""
WSGI config for ferrp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

import sys
sys.path.append('/home/python-www/ferrp')
sys.path.append('/home/python-www/venv/lib/python3.5/site-packages')

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application

from ferrp import settings


#
# # add the virtualenv site-packages path to the sys.path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ferrp.settings")

if settings.DEBUG:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ferrp.settings")
#
# application = get_wsgi_application()