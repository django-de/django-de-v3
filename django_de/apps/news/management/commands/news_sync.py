"""
This command allows the news in the db and on twitter to be synchrnoized.
"""
from optparse import make_option
import logging

from django.core.management.base import BaseCommand, CommandError

from ... import models, utils


LOG = logging.getLogger(__name__)

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
            make_option('--dry-run', action='store_true',
                dest='dryrun', default=False),
            )

    def handle(self, *args, **options):
        last_sync = models.NewsItem.objects.exported()\
                .order_by('-twitter_id')[:1]
        if last_sync:
            last_sync = last_sync[0].twitter_id
        else:
            last_sync = None

        api = utils.get_twitter_api()
        self.import_from_twitter(api, last_sync, options)
        self.export_to_twitter(api, options)

    def import_from_twitter(self, api, last_sync, options):
        LOG.info("Following tweets are imported")
        # TODO: Use cursor
        for tweet in api.user_timeline(since_id=last_sync):
            if tweet.in_reply_to_status_id is not None:
                continue
            LOG.info(" + " + str(tweet.id))
            if options['dryrun']:
                continue
            item = models.NewsItem(title=tweet.text, pub_date=tweet.created_at,
                    twitter_id=tweet.id)
            item.save()

    def export_to_twitter(self, api, options):
        LOG.info("Exporting following news items:")
        for item in models.NewsItem.objects.to_export().order_by('pub_date'):
            LOG.info(" + " + str(item.pk))
            LOG.info("   " + item.as_twitter_message())
            if options['dryrun']:
                continue
            result = api.update_status(item.as_twitter_message())
            if result is not None:
                item.twitter_id = result.id
                LOG.info("     -> " + str(result.id))
                item.save()
