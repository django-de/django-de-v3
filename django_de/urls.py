from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    (r'^', include('django_de.apps.wakawaka.urls')),
    (r'^news/', include('django_de.apps.news.urls')),
    (r'^test', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
)


# Static Media File Serving
if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
    )
