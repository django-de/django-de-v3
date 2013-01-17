from django.contrib import admin

from .models import Event, Source


admin.site.register(Event)
admin.site.register(Source)
