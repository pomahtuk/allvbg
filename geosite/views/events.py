from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from geosite.models import Event


def print_event(request, event_id):
    p = get_object_or_404(Event, pk=event_id)
    return render_to_response('site/main_templates/event.html', {'event': p}, context_instance=RequestContext(request))


