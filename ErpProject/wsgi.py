"""
WSGI config for ErpTaxes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ErpProject.settings')

sys.path.append("/var/www/public_html/ErpTaxes")

application = get_wsgi_application()

"""
from dj_static import Cling
from dj_static import Cling, MediaCling

application = Cling(get_wsgi_application())
application = Cling(MediaCling(get_wsgi_application()))
"""


