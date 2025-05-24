import os
import sys

path = '/home/sarakojima/ProjetPFA'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'GestionCandidatures.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
