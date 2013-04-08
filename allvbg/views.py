from django.shortcuts import get_object_or_404, get_list_or_404, render_to_response, redirect
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from allvbg.models import *
from datetime import *
from django.template import RequestContext, Context
from django import forms
from django.forms.widgets import *
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import *
import re
import hashlib

reg_b = re.compile(r"android|avantgo|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|midp|mmp|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|e\\-|e\\/|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\\-|2|g)|yas\\-|your|zeto|zte\\-", re.I|re.M)
 
 
def is_mobile(request):
	is_mobile = False
	if request.META.has_key('HTTP_USER_AGENT'):
		user_agent = request.META['HTTP_USER_AGENT']
		b = reg_b.search(user_agent)
		v = reg_v.search(user_agent[0:4])
		if b or v:
			#this is a mobile request
			is_mobile =  True
	return is_mobile

def firm_add(request):
  form = FirmForm(request.POST, request.FILES)
  if form.is_valid():
    cmodel = form.save()
    cmodel.pub_date  = datetime.now()
    cmodel.alias     = hashlib.md5(str(datetime.now())).hexdigest()
    cmodel.map_style = MapStyle.objects.get(id=105) #in my database this id belongs to 'empty' style
    cmodel.save()
    return HttpResponseRedirect('/contact/send/')

  return render_to_response('allvbg/firm_form.html', {'form': form}, context_instance=RequestContext(request))

def test_page(request):
	return render_to_response('allvbg/test.html')

#full version functions

def ajax_firm_list(request):
	pagecode = request.GET.get('pagecode')
	if pagecode is not None:
		tmp = get_object_or_404(Firm, pk=pagecode)
		try:
			tmp2 = get_object_or_404(Firm, pk=tmp.parent.id)
			if tmp.container:
				firm_list = Firm.objects.filter(container=False, parent=tmp.id, published=True).order_by("-pub_date")
			else:
				firm_list = Firm.objects.filter(container=False, parent=pagecode, published=True).order_by("-pub_date")
		except:
			firm_list = Firm.objects.filter(container=False, lft__gt=tmp.lft, rght__lt=tmp.rght, published=True).order_by("-pub_date")
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
		
	return render_to_response('allvbg/firm_ajax.html', {'firms': firms, 'lmt':lmt, 'pagecode':pagecode}, context_instance = RequestContext(request))

def calend_ajax(request):
	dt = request.GET.get('date')
	return render_to_response('allvbg/calend_ajax.html', {'y':int(dt.split(',',1)[0]),'m':int(dt.split(',',1)[1])})	

def map_main_xml(request):
	s=MapStyle.objects.order_by('-title')[:500]
	f=Firm.objects.filter(level=0, published=True).order_by("pub_date")
	return render_to_response('allvbg/main_map.xml', {
		'styles':s, 'firms':f
	}, context_instance=RequestContext(request), mimetype="application/xml")
	
def map_unmain_xml(request, firm_id):
	s=MapStyle.objects.order_by('-title')[:500]
	p = get_object_or_404(Firm, Q(published=True), pk=firm_id)
	return render_to_response('allvbg/map.xml', {
		'styles':s,
		'page':p,
	}, context_instance=RequestContext(request), mimetype="application/xml")
	
def contactview(request):
	subject = request.POST.get('topic', '')
	message = request.POST.get('message', '')
	from_email = request.POST.get('email', '')
	name = request.POST.get('name', '')

	if subject and message and name and from_email:
		sbj = 'Message from allvbg.ru. Subject:'+subject
		msg = 'From '+name+':        '+message
		try:
			send_mail(sbj, msg, from_email, ['pman89@ya.ru'])
		except BadHeaderError:
			return HttpResponse('Invalid header found.')
		return HttpResponseRedirect('/contact/send/')
	else:
		return render_to_response('allvbg/contact.html', {'form': ContactForm()},
		RequestContext(request))

	return render_to_response('allvbg/contact.html', {'form': ContactForm()},
		RequestContext(request))

def thankyou(request):
	return render_to_response('allvbg/contact_send.html')

def print_event(request, event_id):
	p = get_object_or_404(Event, pk=event_id)
	return render_to_response('allvbg/main_templates/event.html', {'event':p}, context_instance=RequestContext(request))	

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        frm = Firm.objects.filter(Q(name__search = q)|Q(short__search = q)|Q(meta_key__search = q)).filter(container=False, published=True)
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
        return render_to_response('allvbg/main_templates/search.html', {'firms': firms, 'query': q, 'total':total}, context_instance=RequestContext(request))
    else:
        return render_to_response('allvbg/main_templates/search.html', {'error': True}, context_instance=RequestContext(request))
	
def about(request):
	p = get_object_or_404(Article, pk=1)
	return render_to_response('allvbg/main_templates/event.html', {'event':p}, context_instance=RequestContext(request))			

def articles(request, article_id):
	p = get_object_or_404(Article, pk=article_id)
	return render_to_response('allvbg/main_templates/event.html', {'event':p}, context_instance=RequestContext(request))			

def v1(request, variable_a, variable_b):
	a = get_object_or_404(Firm, Q(published=True), alias=variable_a)
	b = get_object_or_404(Firm, Q(published=True), alias=variable_b)
	if a.level==0 and b.parent.id == a.id:
		return render_to_response('allvbg/main_templates/container.html', {'firm': b},RequestContext(request))	
	else:
		raise Http404
		
def v2(request, variable_a):
	a = get_object_or_404(Firm, Q(published=True), alias=variable_a)
	if a.level == 0:
		return render_to_response('allvbg/main_templates/container.html', {'firm': a},RequestContext(request))
	else:
		raise Http404

def v3(request, variable_a, variable_b, variable_c):
	a = get_object_or_404(Firm, Q(published=True), alias=variable_a)
	b = get_object_or_404(Firm, Q(published=True), alias=variable_b)
	c = get_object_or_404(Firm, Q(published=True), alias=variable_c)
	if c.parent.id==b.id and b.parent.id == a.id:
		return render_to_response('allvbg/main_templates/firm.html', {'firm': c},RequestContext(request))	
	else:
		raise Http404
	
#both version functions
	
def print_page(request, firm_id):
	item = get_object_or_404(Firm, Q(published=True), pk=firm_id)	
	if not is_mobile(request):
		if item.level == 0:
			return render_to_response('allvbg/main_templates/container.html', {'firm': item},RequestContext(request))
		elif item.level == 1:
			return render_to_response('allvbg/main_templates/container.html', {'firm': item},RequestContext(request))
		else:
			return render_to_response('allvbg/main_templates/firm.html', {'firm': item},RequestContext(request))
	else:
		if item.level == 0:
			return render_to_response('allvbg/mobile/mobile_list.html', {'firm': item}, context_instance=RequestContext(request))			
		elif item.level == 1:
			list = get_list_or_404(Firm, parent=item.id)
			return render_to_response('allvbg/mobile/mobile_list_ext.html', {'firm': list}, context_instance=RequestContext(request))			
		else:
			return render_to_response('allvbg/mobile/mobile_item.html', {'firm': item}, context_instance=RequestContext(request))			

def print_main_page(request):
	if not is_mobile(request):
		# return render_to_response('allvbg/mainpage.html', {'firm':0}, context_instance=RequestContext(request))
		return render_to_response('allvbg/main_templates/base.html', {'firm':0}, context_instance=RequestContext(request))
	else:
		return redirect('http://allvbg.ru/mobile/', permanent=True)

#user-admin-site for user-edited content
		
@login_required(login_url='/accounts/login/')
def profile_view(request):
	return render_to_response('allvbg/bootstrap/profile.html', {'user': request.user,}, context_instance=RequestContext(request))			

@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/login/')	
def profile_view_id(request,user_id):
	user = User.objects.get(id=user_id)
	return render_to_response('allvbg/bootstrap/profile.html', {'user': user}, context_instance=RequestContext(request))			

@login_required(login_url='/accounts/login/')
def profile_edit_firm(request, firm_id):
	firm=Firm.objects.get(pk=firm_id)
	if request.user.get_profile().editor_for == firm:
		if request.user.get_profile().paid_till >= datetime.now():
			firm=Firm.objects.get(pk=firm_id)
			return render_to_response('allvbg/bootstrap/firm_edit.html', {'firm': firm}, context_instance=RequestContext(request))			
		else:
			return render_to_response('allvbg/bootstrap/firm_edit.html', context_instance=RequestContext(request))			
	else:
		return HttpResponseRedirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def manage_UserProfile(request):
	a = User.objects.get(pk=request.user.id)
	if request.method == 'POST':
		f = ProfileForm(request.POST, instance=a)
		if f.is_valid():
			f.save()
		return HttpResponseRedirect('/accounts/profile/')
	else:
		f = ProfileForm(instance=a)
		return render_to_response("allvbg/bootstrap/base.html", { "f": f, }, context_instance=RequestContext(request))

@login_required(login_url='/accounts/login/')
def manage_Firm(request):
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
		return render_to_response("allvbg/bootstrap/base.html", { "f": f, }, context_instance=RequestContext(request))
		
#payment functions

def result(request):
	mrh_pass2 = "";
	out_summ = request.GET['OutSum']
	inv_id = request.GET['InvId']
	crc = request.GET['SignatureValue']

	temp = out_summ+":"+inv_id+":"+mrh_pass2		
	my_crc = hashlib.md5(temp).hexdigest()	
	
	if my_crc.upper() == crc.upper():
		msg = "OK"+inv_id+"\n"
	else:
		msg = "bad sign\n"
	return render_to_response("agenda/blank.html", { "msg": msg, },)

def pay(request):

	############################################################
	############################################################
	############################################################
	############################################################

	if request.method == 'POST':
		out_summ=request.POST['OutSum']
		if out_summ=="50":
			mth="1"
		elif out_summ=="90":
			mth="2"
		elif out_summ=="135":
			mth="3"
		elif out_summ=="250":
			mth="6"
		elif out_summ=="450":
			mth="12"
		inv_desc="Payment for editing firm by user with id = "+request.POST['desc']+" for "+mth+" month(s)"
		mrh_login = ""
		mrh_pass1 = ""
		
		m = str(date.today().month)
		if len(m)==1:
			m = "0"+m
		d = str(date.today().day)
		if len(d)==1:
			d = "0"+d		
		y = str(date.today().year)
		
		usr = User.objects.get(pk = request.POST['desc'])
		order = OrdersLisrt(user=usr, summ = out_summ, date = datetime.now(), lng=inv_desc)
		order.save()
		
		inv_id = str(order.id)

		string = mrh_login+":"+out_summ+":"+inv_id+":"+mrh_pass1
		
		crc  = hashlib.md5(string).hexdigest()
		
		#url = "http://test.robokassa.ru/Index.aspx?MrchLogin="+mrh_login+"&OutSum="+out_summ+"&InvId="+inv_id+"&Desc="+inv_desc+"&SignatureValue="+crc;
		
		#uncomment after tests done
		url = "https://merchant.roboxchange.com/Index.aspx?MrchLogin="+mrh_login+"&OutSum="+out_summ+"&InvId="+inv_id+"&Desc="+inv_desc+"&SignatureValue="+crc;
		
		return HttpResponseRedirect(url)
		
def pay_ok(request):
	if request.method == 'GET':
		out_summ = request.GET['OutSum']
		inv_id = request.GET['InvId']
		crc = request.GET['SignatureValue']
		mrh_pass1 = ""
		mrh_login = ""
		mrh_pass2 = ""
		
		temp = out_summ+":"+inv_id+":"+mrh_pass1		
		my_crc = hashlib.md5(temp).hexdigest()
		
		if crc == my_crc:		
			if out_summ=="50":
				mth=1
			elif out_summ=="90":
				mth=2
			elif out_summ=="135":
				mth=3
			elif out_summ=="250":
				mth=6
			elif out_summ=="450":
				mth=12
			
			order = OrdersLisrt.objects.get(pk = inv_id)
			
			y = 0
			if mth == 12:
				mth = 0
				y = 1
				
			dt = datetime(order.date.year+y, order.date.month+mth, order.date.day)
			up = order.user.get_profile()
			up.paid_till = dt
			up.save()
			#return render_to_response("allvbg/bootstrap/base.html", {"dt":dt}, context_instance=RequestContext(request))
			return HttpResponseRedirect('/accounts/profile/')
		else:
			return render_to_response("allvbg/bootstrap/base.html", context_instance=RequestContext(request))
	return HttpResponseRedirect('/accounts/profile/')

#mobile version functions
		
def mobile(request):
	s=MapStyle.objects.order_by('-title')[:500]
	return render_to_response('allvbg/mobile/mobile_index.html', {'styles': s},RequestContext(request))

def mobilesearch(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        frm = Firm.objects.filter(Q(name__search = q)|Q(short__search = q)|Q(meta_key__search = q)).filter(container=False, published=True)
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
        return render_to_response('allvbg/mobile/mobile_search.html', {'firms': firms, 'query': q, 'total':total}, context_instance=RequestContext(request))
    else:
        return render_to_response('allvbg/mobile/mobile_search.html', {'error': True}, context_instance=RequestContext(request))
	
def mobileitem(request, firm_id):
	item = get_object_or_404(Firm, Q(published=True), pk=firm_id)	
	if item.level == 0:
		return render_to_response('allvbg/mobile/mobile_list.html', {'firm': item}, context_instance=RequestContext(request))			
	elif item.level == 1:
		list = get_list_or_404(Firm, parent=item.id)
		return render_to_response('allvbg/mobile/mobile_list_ext.html', {'firm': list}, context_instance=RequestContext(request))			
	else:
		return render_to_response('allvbg/mobile/mobile_item.html', {'firm': item}, context_instance=RequestContext(request))			
	
def mobilemap(request):
	if ('lat' in request.GET and request.GET['lat']) and ('lng' in request.GET and request.GET['lng']):
		lat1 = float(request.GET['lat']) + (0.00001 * 228)
		lng1 = float(request.GET['lng']) + (0.00001 * 228)
		lat2 = float(request.GET['lat']) - (0.00001 * 228)
		lng2 = float(request.GET['lng']) - (0.00001 * 228)		
		firm_list = Firm.objects.filter(container=False, lat__lte=lat1, lat__gte=lat2 ,lng__lte=lng1, lng__gte=lng2, published=True)
		s=MapStyle.objects.order_by('-title')[:500]
		return render_to_response('allvbg/mobile/mobile_map.xml', {
			'styles':s,
			'firm_list':firm_list,
			'lat':request.GET['lat'],
			'lng':request.GET['lng'],
		}, context_instance=RequestContext(request), mimetype="application/xml")
	else:
		raise Http404

#service functions
		
def google_ver(request):
	return render_to_response('agenda/google.html')
		
def sitemap(request):
	return render_to_response('allvbg/sitemap.xml', {'zero': 0}, context_instance=RequestContext(request), mimetype="application/xml")			

def rss(request):
	list=Firm.objects.order_by('-pub_date')[:20]
	return render_to_response('allvbg/rss.xml', {'firms': list}, context_instance=RequestContext(request), mimetype="application/rss+xml")				
	
def widget(request):
    if 'search' in request.GET and request.GET['search']:
        q = request.GET['search']
        frm = Firm.objects.filter(Q(name__search = q)|Q(short__search = q)|Q(meta_key__search = q)).filter(container=False, published=True)
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
        return render_to_response('allvbg/widget.html', {'firms': firms, 'query': q, 'total':total}, context_instance=RequestContext(request))
    else:
        return render_to_response('allvbg/widget.html', {'error': True}, context_instance=RequestContext(request))
		
#caching
	
map_main_xml = cache_page(map_main_xml, 60 * 60)
map_unmain_xml = cache_page(map_unmain_xml, 60 * 60)
mobilemap = cache_page(mobilemap, 60 * 60)
ajax_firm_list = cache_page(ajax_firm_list, 60 * 10)