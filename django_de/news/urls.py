from django.conf.urls import url, patterns

from .views import news_list, news_detail


urlpatterns = patterns('',
    url(r'^(?:(?P<year>\d{4})/(?:(?P<month>\d{2})/(?:(?P<day>\d{2})/)?)?)?$', news_list,
        name='news_list'),
    # url(r'^(?:(?P<year>\d{4})/)?$', news_list,
    #     name='news_list'),
    url(r'^(?P<slug>.*)-(?P<pk>.*)/$', news_detail, name='news_detail'),
)
