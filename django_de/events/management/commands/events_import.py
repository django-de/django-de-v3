from datetime import datetime
import icalendar
import logging
from optparse import make_option
import urllib2

from django.utils import timezone
from django.core.management.base import BaseCommand

from ... import models


LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--dry-run', action='store_true', dest='dryrun', default=False),
    )

    def handle(self, *args, **options):
        LOG.info('Importing calendars')

        for source in models.Source.objects.filter(is_active=True):
            LOG.info('Importing %s' % source.name)

            local_tz = timezone.get_default_timezone()

            try:
                LOG.debug('Fetching calendar from %s' % source.url)
                response = urllib2.urlopen(source.url)
            except urllib2.URLError, error:
                LOG.error(error)
                continue

            try:
                ics = icalendar.Calendar.from_ical(response.read())
            except ValueError, error:
                LOG.error(error)
                continue

            for event in ics.walk('vevent'):
                try:
                    LOG.info(' + %s' % event['summary'].format().encode('utf-8').decode('string-escape'))

                    if options['dryrun']:
                        continue

                    try:
                        start = icalendar.vDatetime.from_ical(event['dtstart'].to_ical()).astimezone(local_tz)
                    except ValueError:
                        start = icalendar.vDate.from_ical(event['dtstart'].to_ical())
                        start = datetime(start.year, start.month, start.day, 0, 0, 0, tzinfo=local_tz)

                    try:
                        end = icalendar.vDatetime.from_ical(event['dtend'].to_ical()).astimezone(local_tz)
                    except ValueError:
                        end = icalendar.vDate.from_ical(event['dtend'].to_ical())
                        end = datetime(end.year, end.month, end.day, 0, 0, 0, tzinfo=local_tz)

                    try:
                        geolocation = event['geo'].to_ical()
                    except KeyError:
                        geolocation = ''

                    obj, created = models.Event.objects.get_or_create(uid=event['uid'], defaults={
                        'title': event['summary'].format().encode('utf-8').decode('string-escape'),
                        'description': event['description'].format().encode('utf-8').decode('string-escape'),
                        'location': event['location'].format().encode('utf-8').decode('string-escape'),
                        'url': event['url'].format().encode('utf-8').decode('string-escape'),
                        'geolocation': geolocation,
                        'start': start,
                        'end': end,
                        'source': source
                    })

                    LOG.info('   -> %s' % ('imported' if created else 'already imported'))
                except Exception, error:
                    # TODO: proper exception handling..
                    LOG.error('%s: %s' % (error.__class__.__name__, error))
                    continue
