from django.conf.urls import patterns, include, url
from allvbgru.views import *
from django.contrib import admin
from django.conf import settings
from filebrowser.sites import site
from allvbg.models import Firm
from djangoratings.views import AddRatingFromModel
from django.conf.urls import *
from tastypie.api import Api
from allvbg.api import FirmResource, MapStyleResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(FirmResource())
v1_api.register(MapStyleResource())


urlpatterns = patterns('',

	url(r'^admin/', include(admin.site.urls)),
	url(r'^admin_tools/', include('admin_tools.urls')),

	url(r'^test/', 'allvbg.views.test_page'),
	url(r'^firm/add/', 'allvbg.views.firm_add'),

	url(r'^api/', include(v1_api.urls)),
	
	url(r'^tinymce/', include('tinymce.urls')),
	url(r'^admin/filebrowser/', include(site.urls)),
	
	url(r'payment/result/$', 'allvbg.views.result'),
	url(r'payment/pay/$', 'allvbg.views.pay'),
	url(r'payment/result_ok/$', 'allvbg.views.pay_ok'),

	url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'allvbg/login.html'}),	
	url(r'^accounts/profile/$', 'allvbg.views.profile_view'),
	url(r'^accounts/profile/edit/$', 'allvbg.views.manage_UserProfile'),
	url(r'^accounts/profile/firm/$', 'allvbg.views.manage_Firm'),
	url(r'^accounts/edit/firm/(?P<firm_id>\d+)/$', 'allvbg.views.profile_edit_firm'),
	url(r'^accounts/profile/(?P<user_id>\d+)/$', 'allvbg.views.profile_view_id'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
	
	url(r'^$', 'allvbg.views.print_main_page'),
	url(r'^(?P<firm_id>\d+)/$', 'allvbg.views.print_page'),			
	url(r'^main_map.xml', 'allvbg.views.map_main_xml'),
	url(r'^map/(?P<firm_id>\d+).xml', 'allvbg.views.map_unmain_xml'),
	url(r'^ajax_list/', 'allvbg.views.ajax_firm_list'),
	url(r'^calend_ajax/', 'allvbg.views.calend_ajax'),
	url(r'^events/(?P<event_id>\d+)/$', 'allvbg.views.print_event'),
	
	url(r'rate/(?P<object_id>\d+)/(?P<score>\d+)/', AddRatingFromModel(), {
		'app_label': 'allvbg',
		'model': 'firm',
		'field_name': 'rating',
	}),	
	
	url(r'^sitemap.xml', 'allvbg.views.sitemap'),	
	url(r'^rss', 'allvbg.views.rss'),
	url(r'^widget.html', 'allvbg.views.widget'),
	url(r'^about.html', 'allvbg.views.about'),
	url(r'^%D0%BE-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B5.html', 'allvbg.views.about'),
	
  url(r'^contact/send/', 'allvbg.views.thankyou'),
  url(r'^contact/', 'allvbg.views.contactview'),	
	url(r'^mobile/(?P<firm_id>\d+)$', 'allvbg.views.mobileitem'),		
	url(r'^article/(?P<article_id>\d+)$', 'allvbg.views.articles'),
	url(r'^search/$', 'allvbg.views.search'),
	
	url(r'^googlec7fb9df20f08fcee.html','allvbg.views.google_ver'),
	
	url(r'^i18n/', include('django.conf.urls.i18n')),	
	
	url(r'^mobile/', 'allvbg.views.mobile'),	
	url(r'^mobile-search/', 'allvbg.views.mobilesearch'),
	url(r'^mobile-map/', 'allvbg.views.mobilemap'),
	
	url(r'^(?P<variable_a>(.+))/(?P<variable_b>(.+))/(?P<variable_c>(.+)).html$', 'allvbg.views.v3'),	
	url(r'^(?P<variable_a>(.+))/(?P<variable_b>(.+))/$', 'allvbg.views.v1'),
	url(r'^(?P<variable_a>(.+))/$', 'allvbg.views.v2'),

)

# if settings.DEBUG:
#     urlpatterns = patterns('',
#     url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#     url(r'', include('django.contrib.staticfiles.urls')),
# ) + urlpatterns
