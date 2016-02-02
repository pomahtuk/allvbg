from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from geosite.models import Firm


def google_ver(request):
    return render_to_response('agenda/google.html', context_instance=RequestContext(request))


def sitemap(request):
    return render_to_response('site/sitemap.xml', {'zero': 0}, context_instance=RequestContext(request),
                              mimetype="application/xml")

def rss(request):
    firm_list = Firm.objects.order_by('-pub_date')[:20]
    return render_to_response('site/rss.xml', {'firms': firm_list}, context_instance=RequestContext(request),
                              mimetype="application/rss+xml")

def test_page(request):
    return render_to_response('site/test.html', context_instance=RequestContext(request))


def calendar_ajax(request):
    dt = request.GET.get('date')
    return render_to_response('site/calend_ajax.html', {'y': int(dt.split(',', 1)[0]), 'm': int(dt.split(',', 1)[1])})


def widget(request):
    if 'search' in request.GET and request.GET['search']:
        q = request.GET['search']
        condition = Q(name__search=q) | Q(short__search=q) | Q(meta_key__search=q)
        frm = Firm.objects.filter(condition).filter(container=False, published=True)
        total = frm.count()
        page = request.GET.get('page')
        if page is not None:
            pg = int(page)
        else:
            pg = 1
        paginator = Paginator(frm, 4)

        try:
            firms = paginator.page(pg)
        except PageNotAnInteger:
            firms = paginator.page(1)
        except EmptyPage:
            firms = paginator.page(paginator.num_pages)

        return render_to_response('site/widget.html', {'firms': firms, 'query': q, 'total':total}, context_instance=RequestContext(request))
    else:
        return render_to_response('site/widget.html', {'error': True}, context_instance=RequestContext(request))
