from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import gettext_lazy as _


class NewsItemManager(models.Manager):
    def to_export(self):
        """
        Filters all items, that haven't been exported yet.
        """
        return self.filter(twitter_id__isnull=True)


class NewsItem(models.Model):
    """
    A basic news item. The title is mostly something that can end up on
    services like Twitter. If the body is not empty, the exteral
    representation of such an item also includes a link to the post
    and a respectively shortened title.
    """
    title = models.CharField(verbose_name=_("title"), max_length=140)
    body = models.TextField(verbose_name=_("body"), blank=True, null=True)
    pub_date = models.DateTimeField(verbose_name=_("published at"),
            auto_now_add=True)
    author = models.ForeignKey(User, verbose_name=_("author"))

    twitter_id = models.IntegerField(verbose_name=_("Twitter ID"),
            blank=True, null=True)

    objects = NewsItemManager()

    def as_twitter_message(self):
        if self.body is None:
            return self.title
        item_url = 'http://%s/n/%s' % (
            Site.objects.get_current().domain,
            str(self.pk)
            )
        return self.title[:-(len(item_url)+4)] + '... ' + item_url

