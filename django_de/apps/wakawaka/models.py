from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from glob import glob
from os.path import abspath, split

def _get_wiki_template_choices():
    templates = glob('%s/*.html' % settings.WAKAWAKA_TEMPLATE_DIR)
    choices = [(abspath(t), split(t)[1]) for t in templates]
    return choices

TEMPLATE_CHOICES = _get_wiki_template_choices()

class WikiPage(models.Model):
    slug = models.CharField(_('slug'), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    template = models.CharField(_('Template'), max_length=1000, choices=TEMPLATE_CHOICES,
                                default=settings.WAKAWAKA_TEMPLATE_DEFAULT)

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return self.slug

    @property
    def current(self):
        return self.revisions.latest()

    def rev(self, rev_id):
        return self.revisions.get(pk=rev_id)

class Revision(models.Model):
    page = models.ForeignKey(WikiPage, related_name='revisions')
    content = models.TextField(_('content'))
    message = models.TextField(_('change message'), blank=True)
    creator = models.ForeignKey(User, blank=True, null=True)
    creator_ip = models.IPAddressField(_('creator ip'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        ordering = ['-modified']
        get_latest_by = 'modified'

    def __unicode__(self):
        return 'Revision %s for %s' % (self.created.strftime('%Y%m%d-%H%M'), self.page.slug)
