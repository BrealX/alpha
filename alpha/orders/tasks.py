# Tasks for Celery here
from __future__ import absolute_import, unicode_literals
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from orders.utils import scrapers
from celery.utils.log import get_task_logger
from datetime import datetime


logger = get_task_logger(__name__)


# A periodic task that will run every Sunday noon
@periodic_task(run_every=(crontab(hour="10", minute="27", day_of_week="mon-fri")))
def scraper_areas():
    logger.info('Starting collecting Areas from Delivery API')
    now = datetime.now()
    task = scrapers.get_areas()
    time = now.day + now.minute
    logger.info('Task finished at %i' % time)


# A periodic task that will run every Sunday 12:05 pm
@periodic_task(run_every=(crontab(hour="12", minute="5", day_of_week="6")))
def scraper_cities():
    logger.info('Starting collecting Cities from Delivery API')
    now = datetime.now()
    task = scrapers.get_cities()
    time = now.day + now.minute
    logger.info('Task finished at %i' % time)