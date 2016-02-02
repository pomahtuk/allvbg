from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from geosite.models import Firm, MapStyle
from geosite.forms import FirmForm

import hashlib
from datetime import *


def firm_add(request):
    error = False
    if request.method == 'GET':
        form = FirmForm()
    else:
        form = FirmForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                cmodel = form.save()
                cmodel.pub_date = datetime.now()
                cmodel.alias = hashlib.md5(str(datetime.now())).hexdigest()
                cmodel.map_style = MapStyle.objects.get(id=105)  # in my database this id belongs to 'empty' style
                cmodel.save()
                return HttpResponseRedirect('/contact/send/')
            except:
                error = True
                print >> sys.stderr, 'empty parent'
        else:
            error = True
    return render_to_response('site/firm_form.html', {'form': form, 'error': error},
                              context_instance=RequestContext(request))


@cache_page(60 * 10)
def ajax_firm_list(request):
    pagecode = request.GET.get('pagecode')
    if pagecode is not None:
        tmp = get_object_or_404(Firm, pk=pagecode)
        try:
            if tmp.container:
                firm_list = Firm.objects.filter(container=False, parent=tmp.id, published=True).order_by("-pub_date")
            else:
                firm_list = Firm.objects.filter(container=False, parent=pagecode, published=True).order_by("-pub_date")
        except:
            firm_list = Firm.objects.filter(container=False, lft__gt=tmp.lft, rght__lt=tmp.rght,
                                            published=True).order_by("-pub_date")
    else:
        firm_list = Firm.objects.filter(container=False, published=True).order_by("-pub_date")

    limit = request.GET.get('limit')
    if limit is not None:
        lmt = int(limit)
    else:
        lmt = 12

    page = request.GET.get('page')
    if page is not None:
        pg = int(page)
    else:
        pg = 1
    paginator = Paginator(firm_list, lmt)

    try:
        firms = paginator.page(pg)
    except PageNotAnInteger:
        firms = paginator.page(1)
    except EmptyPage:
        firms = paginator.page(paginator.num_pages)

    return render_to_response('site/firm_ajax.html', {'firms': firms, 'lmt': lmt, 'pagecode': pagecode},
                              context_instance=RequestContext(request))


# TODO: this should be one function
def v1(request, variable_a, variable_b):
    a = get_object_or_404(Firm, Q(published=True), alias=variable_a)
    b = get_object_or_404(Firm, Q(published=True), alias=variable_b)
    if a.level == 0 and b.parent.id == a.id:
        return render_to_response('site/main_templates/container.html', {'firm': b}, RequestContext(request))
    else:
        raise Http404


def v2(request, variable_a):
    a = get_object_or_404(Firm, Q(published=True), alias=variable_a)
    if a.level == 0:
        return render_to_response('site/main_templates/container.html', {'firm': a}, RequestContext(request))
    else:
        raise Http404


def v3(request, variable_a, variable_b, variable_c):
    a = get_object_or_404(Firm, Q(published=True), alias=variable_a)
    b = get_object_or_404(Firm, Q(published=True), alias=variable_b)
    c = get_object_or_404(Firm, Q(published=True), alias=variable_c)
    if c.parent.id == b.id and b.parent.id == a.id:
        return render_to_response('site/main_templates/firm.html', {'firm': c}, RequestContext(request))
    else:
        raise Http404

