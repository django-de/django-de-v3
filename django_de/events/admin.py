from django.contrib import admin

from .models import Event, Source


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'end', 'slug']
    date_hierarchy = 'start'


class SourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'is_active']
    list_filter = ['is_active']


admin.site.register(Event, EventAdmin)
admin.site.register(Source, SourceAdmin)
