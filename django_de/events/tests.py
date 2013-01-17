import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError

from . import models


class EventTests(TestCase):
    def test_end_after_or_same_as_start(self):
        """
        The end of an event has to be after or at the same time as the start.
        """
        start =  timezone.now()
        evt = models.Event(uid="TEST", title="TEST")
        with self.assertRaises(ValidationError):
            evt.start = start
            evt.end = start - datetime.timedelta(days=1)
            evt.full_clean()
        evt.end = start
        evt.full_clean()
        evt.end = start + datetime.timedelta(days=1)
        evt.full_clean()
