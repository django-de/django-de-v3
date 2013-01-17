from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    uid = models.CharField(_('UID'), unique=True, max_length=255)

    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(verbose_name=_('Slug'), blank=True)
    description = models.TextField(_('Description'), blank=True)
    location = models.TextField(_('Location'), blank=True)

    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))

    url = models.CharField(_('URL'), max_length=255, blank=True)
    geolocation = models.CharField(_('GEO Location'), max_length=32, blank=True)

    source = models.ForeignKey('Source', verbose_name=_('Source'), blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = slugify(self.title[:30])

        return super(Event, self).save(*args, **kwargs)

    def clean(self):
        if self.start > self.end:
            raise ValidationError(_('Start date after end date.'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('start', 'end', 'title')


class Source(models.Model):
    name = models.CharField(_('Name'), max_length=32)
    url = models.CharField(_('URL'), max_length=255)
    is_active = models.BooleanField(_('Is active?'), default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Source')
