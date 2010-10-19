from django.contrib import admin

from . import models


class NewsItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_display = ('truncated_title', 'pub_date', 'author', 'twitter_id',)
    list_filter = ('pub_date',)

    def truncated_title(self, obj):
        if len(obj.title) < 50:
            return obj.title
        return obj.title[:47] + '...'

admin.site.register(models.NewsItem, NewsItemAdmin)
