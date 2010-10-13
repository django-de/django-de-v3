from django.template import RequestContext
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models.query import Q

from . import models


def index(request, year=None, month=None, day=None, template_name=None,
        page_size=None, page_param=None):
    """
    A simple index view that can be restricted to a certain year, year+month or
    year+month+day.
    """
    if template_name is None:
        template_name = 'news/index.html'
    if page_size is None:
        page_size = getattr(settings, "PAGINATION_DEFAULT_PAGINATION", 20)
    if page_param is None:
        page_param = 'page'
    page_num = int(request.GET.get(page_param, 1))
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
    paginator = Paginator(query.order_by('-pub_date'),
            page_size)
    page = paginator.page(page_num)
    return render_to_response(template_name, {
        'page_obj': page,
        'paginator': page.paginator,
        },
        context_instance=RequestContext(request))

def view_item(request, pk, slug=None, template_name=None):
    """
    Presents a single newsitem.
    """
    if template_name is None:
        template_name = 'news/view.html'
    item = get_object_or_404(models.NewsItem.objects, pk=pk)
    return render_to_response(template_name, {
        'item': item,
        }, context_instance=RequestContext(request))
    pass
