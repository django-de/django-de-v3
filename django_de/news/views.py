from django.db.models.query import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from . import models


def news_list(request, year=None, month=None, day=None):
    """
    A simple index view that can be restricted to a certain year, year+month or
    year+month+day.
    """
    query = models.NewsItem.objects
    filter_ = Q()
    if year is not None:
        filter_ &= Q(pub_date__year=int(year))
    if month is not None:
        filter_ &= Q(pub_date__month=int(month))
    if day is not None:
        filter_ &= Q(pub_date__day=int(day))
    if filter_ is not None:
        query = query.filter(filter_)

    return render(request, 'news/list.html', {
        'object_list': query,
        'months': models.NewsItem.objects.dates('pub_date', 'month',
                                                order='DESC'),
    })


def news_detail(request, pk, slug=None):
    """
    Presents a single newsitem.
    """
    item = get_object_or_404(models.NewsItem.objects, pk=pk)

    return render(request, 'news/detail.html', {
        'object': item,
    })


def news_shortcut(request, pk):
    item = get_object_or_404(models.NewsItem.objects, pk=pk)
    return HttpResponseRedirect(item.get_absolute_url())
