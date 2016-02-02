from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from geosite.models import Firm, MapStyle


@cache_page(60 * 60)
def map_main_xml(request):
    s = MapStyle.objects.order_by('-title')[:500]
    f = Firm.objects.filter(level=0, published=True).order_by("pub_date")
    return render_to_response('site/main_map.xml', {
        'styles': s, 'firms': f
    }, context_instance=RequestContext(request), mimetype="application/xml")


def map_json(request):
    callback = request.GET.get('callback', '')
    s = MapStyle.objects.order_by('-title')[:500]
    f = Firm.objects.filter(level=0, published=True).order_by("pub_date")
    return render_to_response('site/map.json', {
        'styles': s, 'firms': f, 'callback': callback
    }, context_instance=RequestContext(request), mimetype="application/json")


@cache_page(60 * 60)
def map_unmain_xml(request, firm_id):
    s = MapStyle.objects.order_by('-title')[:500]
    p = get_object_or_404(Firm, Q(published=True), pk=firm_id)
    return render_to_response('site/map.xml', {
        'styles': s,
        'page': p,
    }, context_instance=RequestContext(request), mimetype="application/xml")