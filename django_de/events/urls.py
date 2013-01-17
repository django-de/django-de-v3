from django.conf.urls.defaults import url, patterns

from .views import events_list


urlpatterns = patterns('',
    url(r'^((?P<year>\d{4})/((?P<month>\d{2})/((?P<day>\d{2})/)?)?)?$', events_list,
        name='events_list'),
)
