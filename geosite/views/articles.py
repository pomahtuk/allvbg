from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from geosite.models import Article


def about(request):
    p = get_object_or_404(Article, pk=1)
    return render_to_response('site/main_templates/event.html', {'event': p}, context_instance=RequestContext(request))


def articles(request, article_id):
    p = get_object_or_404(Article, pk=article_id)
    return render_to_response('site/main_templates/event.html', {'event': p}, context_instance=RequestContext(request))
