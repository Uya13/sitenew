import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_thursday_at_time': {
        'task': 'news.tasks.weekly_mailing',
        'schedule': crontab(hour=15, minute=3, day_of_week=4),
    },
}

# app.conf.beat_schedule = {
#     'action_every_thursday_12pm': {
#         'task': 'news.tasks.weekly_mailing',
#         'schedule': crontab(hour=14, minute=55, day_of_week=4),
#     },
# }

# app.conf.beat_schedule = {
#     'action_every_thursday_12pm': {
#         'task': 'news.tasks.weekly_sending',
#         'schedule': crontab(hour=12, minute=8, day_of_week='thursday'),
#     },
# }