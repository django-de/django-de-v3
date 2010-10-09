from django.contrib.auth.decorators import login_required
from django_de.apps.wakawaka.urls import urlpatterns

for waka_url in urlpatterns:
    callback = waka_url.callback
    waka_url._callback = login_required(callback)
