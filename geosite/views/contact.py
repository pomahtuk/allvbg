from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect, HttpResponse

from geosite.forms import ContactForm


def contact_view(request):
    subject = request.POST.get('topic', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('email', '')
    name = request.POST.get('name', '')

    # TODO: get from db
    if subject and message and name and from_email:
        sbj = 'Message from  Subject:' + subject
        msg = 'From ' + name + ':        ' + message
        try:
            send_mail(sbj, msg, from_email, ['pman89@ya.ru'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/send/')
    else:
        return render_to_response('site/contact.html', {'form': ContactForm()},
                                  RequestContext(request))

    return render_to_response('site/contact.html', {'form': ContactForm()},
                              RequestContext(request))


def thank_you(request):
    return render_to_response('site/contact_send.html', RequestContext(request))
