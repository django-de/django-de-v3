from datetime import date

from django.db.models.query import Q
from django.shortcuts import render

from . import models


def events_list(request, year=None, month=None, day=None):
    """
    A simple index view that can be restricted to a certain year, year+month or
    year+month+day.
    """
    query = models.Event.objects
    filter_ = Q()
    if year is not None:
        filter_ &= Q(start__year=int(year))
    if month is not None:
        filter_ &= Q(start__month=int(month))
    if day is not None:
        filter_ &= Q(start__day=int(day))
    if filter_ is not None:
        query = query.filter(filter_)

    query = query.filter(start__gte=date.today()).order_by('start')
    return render(request, 'events/list.html', {
        'object_list': query,
    })
