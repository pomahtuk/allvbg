from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404

from geosite.models import User, Firm
from geosite.forms import ProfileForm, FirmUserForm

from datetime import *


# user-admin-geosite for user-edited content
@login_required(login_url='/accounts/login/')
def profile_view(request):
    return render_to_response('site/bootstrap/profile.html', {'user': request.user, },
                              context_instance=RequestContext(request))

# TODO: only superuser now could edit profiles fix
@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')
def profile_view_id(request, user_id):
    user = User.objects.get(id=user_id)
    return render_to_response('site/bootstrap/profile.html', {'user': user}, context_instance=RequestContext(request))


@login_required(login_url='/accounts/login/')
def profile_edit_firm(request, firm_id):
    firm = Firm.objects.get(pk=firm_id)
    if request.user.get_profile().editor_for == firm:
        if request.user.get_profile().paid_till >= datetime.now():
            firm = Firm.objects.get(pk=firm_id)
            return render_to_response('site/bootstrap/firm_edit.html', {'firm': firm},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('site/bootstrap/firm_edit.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/accounts/login/')


@login_required(login_url='/accounts/login/')
def manage_user_profile(request):
    a = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        f = ProfileForm(request.POST, instance=a)
        if f.is_valid():
            f.save()
        return HttpResponseRedirect('/accounts/profile/')
    else:
        f = ProfileForm(instance=a)
        return render_to_response("site/bootstrap/base.html", {"f": f, }, context_instance=RequestContext(request))


@login_required(login_url='/accounts/login/')
def manage_firm(request):
    a = request.user.get_profile().editor_for
    if request.method == 'POST':
        f = FirmUserForm(request.POST, request.FILES, instance=a)
        if f.is_valid():
            f.save()
        else:
            return HttpResponseRedirect('/accounts/login/')
        return HttpResponseRedirect('/accounts/profile/')
    else:
        f = FirmUserForm(instance=a)
        return render_to_response("site/bootstrap/base.html", {"f": f, }, context_instance=RequestContext(request))

