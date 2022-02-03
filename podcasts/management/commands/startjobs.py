# podcasts/management/commands/startjobs.py
# Standard library
from datetime import timezone
import logging

# Django library
from django.conf import settings
from django.core.management.base import BaseCommand


# Third party 
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from podcasts.models import Episode

logger = logging.getLogger(__name__)

def save_new_episodes(feed):
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image['href']

    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            episode = Episode(
                title = item.title,
                description = item.description,
                pub_date = parser.parse(item.published),
                link =item.link,
                image = podcast_image,
                podcast_name = podcast_title,
                guid = item.guid
            )

            episode.save()


def fetch_realpython_episodes():
    """Fetches new episodes from RSS for The Real Python Podcast."""
    _feed = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
    save_new_episodes(_feed)

# https://www.spreaker.com/show/4940884/episodes/feed
# https://feeds.simplecast.com/WpQaX_cs
# https://feeds.transistor.fm/the-built-with-django-podcast

def fetch_django_stars_episodes():
    """Fetches new episodes from RSS for Django Stars Podcast."""
    _feed = feedparser.parse("https://www.spreaker.com/show/4940884/episodes/feed")
    save_new_episodes(_feed)

def fetch_django_riffs_episodes():
    """Fetches new episodes from RSS for Django Riffs Podcast."""
    _feed = feedparser.parse("https://feeds.simplecast.com/l_5sU3vk")
    save_new_episodes(_feed)

def fetch_talkpython_episodes():
    """Fetches new episodes from RSS for the Talk Python to Me Podcast."""
    _feed = feedparser.parse("https://talkpython.fm/episodes/rss")
    save_new_episodes(_feed)

def delete_old_execution_jobs(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler =  BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_realpython_episodes,
            trigger='interval',
            minutes=2,
            id="The Real Python Podcast",
            max_instances=1,
            replace_existing=True
        )

        logger.info("Added job: The Real Python Podcast.")
    
        scheduler.add_job(
            fetch_talkpython_episodes,
            trigger='interval',
            minutes=2,
            id="The Talk Python Podcast",
            max_instances=1,
            replace_existing=True
        )

        logger.info("Added job: The Talk Python Podcast.")

        scheduler.add_job(
            fetch_django_riffs_episodes,
            trigger='interval',
            minutes=2,
            id="The Django Riffs Podcast",
            max_instances=1,
            replace_existing=True
        )

        logger.info("Added job: The Django Riffs Podcast.")

        scheduler.add_job(
            fetch_django_stars_episodes,
            trigger='interval',
            minutes=2,
            id="The Django Stars Podcast",
            max_instances=1,
            replace_existing=True
        )

        logger.info("Added job: The Django Stars Podcast.")

        scheduler.add_job(
            delete_old_execution_jobs,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="Delete Old Execution Jobs",
            max_instances=1,
            replace_existing=True
        )

        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Scheduler stopping...")
            scheduler.shutdown()
            logger.info("Scheduler shutdwon sucessfully.")

