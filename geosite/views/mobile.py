from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404

from geosite.models import MapStyle, Firm


def mobile(request):
    s = MapStyle.objects.order_by('-title')[:500]
    return render_to_response('site/mobile/mobile_index.html', {'styles': s}, RequestContext(request))


def mobile_search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        frm = Firm.objects.filter(Q(name__search=q) | Q(short__search=q) | Q(meta_key__search=q)).filter(
            container=False, published=True)
        total = frm.count()
        page = request.GET.get('page')
        if page is not None:
            pg = int(page)
        else:
            pg = 1
        paginator = Paginator(frm, 10)

        try:
            firms = paginator.page(pg)
        except PageNotAnInteger:
            firms = paginator.page(1)
        except EmptyPage:
            firms = paginator.page(paginator.num_pages)
        return render_to_response('site/mobile/mobile_search.html', {'firms': firms, 'query': q, 'total': total},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('site/mobile/mobile_search.html', {'error': True},
                                  context_instance=RequestContext(request))


def mobile_item(request, firm_id):
    item = get_object_or_404(Firm, Q(published=True), pk=firm_id)
    if item.level == 0:
        return render_to_response('site/mobile/mobile_list.html', {'firm': item},
                                  context_instance=RequestContext(request))
    elif item.level == 1:
        firm_list = get_list_or_404(Firm, parent=item.id)
        return render_to_response('site/mobile/mobile_list_ext.html', {'firm': firm_list},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('site/mobile/mobile_item.html', {'firm': item},
                                  context_instance=RequestContext(request))


@cache_page(60 * 60)
def mobile_map(request):
    if ('lat' in request.GET and request.GET['lat']) and ('lng' in request.GET and request.GET['lng']):
        lat1 = float(request.GET['lat']) + (0.00001 * 228)
        lng1 = float(request.GET['lng']) + (0.00001 * 228)
        lat2 = float(request.GET['lat']) - (0.00001 * 228)
        lng2 = float(request.GET['lng']) - (0.00001 * 228)
        firm_list = Firm.objects.filter(container=False, lat__lte=lat1, lat__gte=lat2, lng__lte=lng1, lng__gte=lng2,
                                        published=True)
        s = MapStyle.objects.order_by('-title')[:500]
        return render_to_response('site/mobile/mobile_map.xml', {
            'styles': s,
            'firm_list': firm_list,
            'lat': request.GET['lat'],
            'lng': request.GET['lng'],
        }, context_instance=RequestContext(request), mimetype="application/xml")
    else:
        raise Http404

