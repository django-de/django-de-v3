from django.conf.urls.defaults import *

from .views import index, view_item


urlpatterns = patterns('',
    url(r'^((?P<year>\d{4})/((?P<month>\d{2})/((?P<day>\d{2})/)?)?)?$', index,
        name='news_index'),
    url(r'^(?P<slug>.*)\.(?P<pk>.*)$', view_item, name='news_item'),
    )
