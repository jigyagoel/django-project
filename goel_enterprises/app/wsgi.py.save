"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/lucifer/Dev/goel_enterprises/env/lib/python3.6/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/lucifer/Dev/goel_enterprises/')
sys.path.append('/home/lucifer/Dev/goel_enterprises/app')

#to set enviroment settings for Django apps
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'

# Activate your virtual env
activate_env=os.path.expanduser('/home/lucifer/Dev/goel_enterprises/env/bin/activate_this.py')
exec(open(activate_env).read(), {'__file__': activate_env})

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()
