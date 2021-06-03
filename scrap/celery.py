from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
# from scrap import productions

# set the default Django settings module for the 'celery' program.
# try:
# 	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrap.productions')
# except:
# 	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrap.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrap.settings')
app = Celery('scrap')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))