from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from geosite.models import *
from django.template import RequestContext
from django.db.models import Q
import re

###
from django.db import connection
from django.conf import settings
###

reg_b = re.compile(
    r"android|avantgo|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|midp|mmp|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino",
    re.I | re.M)
reg_v = re.compile(
    r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|e\\-|e\\/|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\\-|2|g)|yas\\-|your|zeto|zte\\-",
    re.I | re.M)


def is_mobile(request):
    is_mobile_client = False
    if 'HTTP_USER_AGENT' in request.META:
        user_agent = request.META['HTTP_USER_AGENT']
        b = reg_b.search(user_agent)
        v = reg_v.search(user_agent[0:4])
        if b or v:
            # this is a mobile request
            is_mobile_client = True
    return is_mobile_client


def search(request):
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
        return render_to_response('site/main_templates/search.html', {'firms': firms, 'query': q, 'total': total},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response('site/main_templates/search.html', {'error': True},
                                  context_instance=RequestContext(request))

# both version functions

def print_page(request, firm_id):
    item = get_object_or_404(Firm, Q(published=True), pk=firm_id)
    if not is_mobile(request):
        if item.level == 0:
            return render_to_response('site/main_templates/container.html', {'firm': item}, RequestContext(request))
        elif item.level == 1:
            return render_to_response('site/main_templates/container.html', {'firm': item}, RequestContext(request))
        else:
            return render_to_response('site/main_templates/firm.html', {'firm': item}, RequestContext(request))
    else:
        if item.level == 0:
            return render_to_response('site/mobile/mobile_list.html', {'firm': item},
                                      context_instance=RequestContext(request))
        elif item.level == 1:
            list = get_list_or_404(Firm, parent=item.id)
            return render_to_response('site/mobile/mobile_list_ext.html', {'firm': list},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('site/mobile/mobile_item.html', {'firm': item},
                                      context_instance=RequestContext(request))


def print_main_page(request):
    if not is_mobile(request):
        return render_to_response('site/main_templates/base.html', {'firm': 0},
                                  context_instance=RequestContext(request))
    else:
        # TODO: use urls from settings
        return redirect('http://geosite.ru/mobile/', permanent=True)
