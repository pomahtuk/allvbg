from django.conf.urls import patterns, include, url
from views import *
from django.contrib import admin
from django.conf import settings
from filebrowser.sites import site
from django.conf.urls import url
from admin_tools import urls as admin_tools_urls
from tinymce import urls as tinymce_urls
from geo_site import views

# from tastypie.api import Api

# from geo_site.geo_site.api import FirmResource, MapStyleResource

admin.autodiscover()

# v1_api = Api(api_name='v1')
# v1_api.register(FirmResource())
# v1_api.register(MapStyleResource())


urlpatterns = ['',

	url(r'^admin/', include(admin.site.urls)),
	url(r'^admin_tools/', include(admin_tools_urls)),

	url(r'^agent/', views.indexisto_agent),

	url(r'^test/', views.test_page),
	url(r'^firm/add/', views.firm_add),

	# url(r'^api/', include(v1_api.urls)),

	url(r'^tinymce/', include(tinymce_urls)),
	# url(r'^admin/filebrowser/', include(geo_site.urls)),

	url(r'payment/result/$', views.result),
	url(r'payment/pay/$', views.pay),
	url(r'payment/result_ok/$', views.pay_ok),

	url(r'^accounts/login/$', django.contrib.auth.views.login, {'template_name': 'geo_site/login.html'}),
	url(r'^accounts/profile/$', views.profile_view),
	url(r'^accounts/profile/edit/$', views.manage_UserProfile),
	url(r'^accounts/profile/firm/$', views.manage_Firm),
	url(r'^accounts/edit/firm/(?P<firm_id>\d+)/$', views.profile_edit_firm),
	url(r'^accounts/profile/(?P<user_id>\d+)/$', views.profile_view_id),
	url(r'^accounts/logout/$', django.contrib.auth.views.logout_then_login),

	url(r'^$', views.print_main_page),
	url(r'^(?P<firm_id>\d+)/$', views.print_page),
	url(r'^main_map.xml', views.map_main_xml),
	url(r'^map.json', views.map_json),
	url(r'^map/(?P<firm_id>\d+).xml', views.map_unmain_xml),
	url(r'^ajax_list/', views.ajax_firm_list),
	url(r'^calend_ajax/', views.calend_ajax),
	url(r'^events/(?P<event_id>\d+)/$', views.print_event),

	url(r'^sitemap.xml', views.sitemap),
	url(r'^rss', views.rss),
	url(r'^widget.html', views.widget),
	url(r'^about.html', views.about),
	url(r'^%D0%BE-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B5.html', views.about),

	url(r'^contact/send/', views.thankyou),
	url(r'^contact/', views.contactview),
	url(r'^mobile/(?P<firm_id>\d+)$', views.mobileitem),
	url(r'^article/(?P<article_id>\d+)$', views.articles),
	url(r'^search/$', views.search),

	url(r'^googlec7fb9df20f08fcee.html', views.google_ver),

	url(r'^i18n/', include(django.conf.urls.i18n)),

	url(r'^mobile/', views.mobile),
	url(r'^mobile-search/', views.mobilesearch),
	url(r'^mobile-map/', views.mobilemap),

	url(r'^(?P<variable_a>(.+))/(?P<variable_b>(.+))/(?P<variable_c>(.+)).html$', views.v3),
	url(r'^(?P<variable_a>(.+))/(?P<variable_b>(.+))/$', views.v1),
	url(r'^(?P<variable_a>(.+))/$', views.v2),

]

# if settings.DEBUG:
#     urlpatterns = patterns('',
#     url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#     url(r'', include('django.contrib.staticfiles.urls')),
# ) + urlpatterns
