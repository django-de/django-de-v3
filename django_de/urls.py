from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    #(r'^', include('django_de.apps.wakawaka.urls')),
    (r'^news/', include('django_de.news.urls')),
    url(r'^n/(?P<pk>.*)/$', 'django_de.news.views.news_shortcut',
        name='news_shortcut'),

    (r'^events/', include('django_de.events.urls')),

    (r'^$', TemplateView.as_view(template_name='home.html')),
)
