from django.test import TestCase
from django.contrib.auth.models import User

from . import models


class BasicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')
    def testTwitterMessage(self):
        item = models.NewsItem()
        item.title = "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 "
        self.assertEquals(item.as_twitter_message(), item.title)

        item.body = "123"
        item.author = self.user
        item.save()
        expected = "123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 1234... http://example.com/n/1"
        self.assertEquals(expected, item.as_twitter_message())

    def testToExport(self):
        a = models.NewsItem(title="a", author=self.user)
        b = models.NewsItem(title="b", author=self.user)
        a.save()
        b.save()
        self.assertEquals(2, len(models.NewsItem.objects.to_export()))
        b.twitter_id="123"
        b.save()
        self.assertEquals(1, len(models.NewsItem.objects.to_export()))
