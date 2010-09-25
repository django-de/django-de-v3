from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Member(models.Model):
    """

    first_name, last_name and email are found in the user relation.
    """
    user = models.OneToOneField(User)
    street = models.CharField(_('Street'), max_length=100)
    zip_code = models.CharField(_('ZIP Code'), max_length=100)
    city = models.CharField(_('City'), max_length=100)
    country = models.CharField(_('Country'), max_length=100, choices=settings.LANGUAGES)
    phone = models.CharField(_('Phone Number'), max_length=100, blank=True, null=True)

    company = models.BooleanField(_('Is a company'), default=False)
    company_names = models.TextField(_('Additional member names of a company'), blank=True, null=True)

    date_entry = models.DateField(_('Entry date'))
    date_exit = models.DateField(_('Exit date'), blank=True, null=True)

    def __unicode__(self):
        return 'Member profile for %s' % self.user.username
