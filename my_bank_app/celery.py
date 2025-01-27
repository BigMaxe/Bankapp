from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

#set the deafult django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_bank_app.settings')

app = Celery('my_bank_app')

#using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a 'CELERY_' prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

#LOAD TASK MODULES FROM ALL REGISTERED DJANGO APP CONFIGS.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'calculate_interest': {
        'task': 'calculate_interest',
        #http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
        'schedule': crontab(0, 0, day_of_month='1'),
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
    