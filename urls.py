from django.conf.urls import patterns, include, url, i18n
from django.contrib.auth.views import login, logout_then_login
from django.contrib import admin
from django.conf import settings
from filebrowser.sites import site
from django.conf.urls import url
from admin_tools import urls as admin_tools_urls
from tinymce import urls as tinymce_urls
from geosite import views

# from tastypie.api import Api

# from geosite.geosite.api import FirmResource, MapStyleResource

admin.autodiscover()

# v1_api = Api(api_name='v1')
# v1_api.register(FirmResource())
# v1_api.register(MapStyleResource())


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include(admin_tools_urls)),

    url(r'^test/', views.test_page),
    url(r'^firm/add/', views.firm_add),

    # url(r'^api/', include(v1_api.urls)),

    url(r'^tinymce/', include(tinymce_urls)),

    url(r'payment/result/$', views.result),
    url(r'payment/pay/$', views.pay),
    url(r'payment/result_ok/$', views.pay_ok),

    url(r'^accounts/login/$', login, {'template_name': 'site/login.html'}),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/profile/$', views.profile_view),
    url(r'^accounts/profile/edit/$', views.manage_user_profile),
    url(r'^accounts/profile/firm/$', views.manage_firm),
    url(r'^accounts/edit/firm/(?P<firm_id>\d+)/$', views.profile_edit_firm),
    url(r'^accounts/profile/(?P<user_id>\d+)/$', views.profile_view_id),

    url(r'^$', views.print_main_page),
    url(r'^(?P<firm_id>\d+)/$', views.print_page),
    url(r'^main_map.xml', views.map_main_xml),
    url(r'^map.json', views.map_json),
    url(r'^map/(?P<firm_id>\d+).xml', views.map_unmain_xml),
    url(r'^ajax_list/', views.ajax_firm_list),
    url(r'^calend_ajax/', views.calendar_ajax),
    url(r'^events/(?P<event_id>\d+)/$', views.print_event),

    # seo part
    url(r'^sitemap.xml', views.sitemap),
    url(r'^rss', views.rss),
    # yandex widget
    url(r'^widget.html', views.widget),

    url(r'^about.html', views.about),
    url(r'^%D0%BE-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B5.html', views.about),

    url(r'^contact/send/', views.thank_you),
    url(r'^contact/', views.contact_view),
    url(r'^article/(?P<article_id>\d+)$', views.articles),
    url(r'^search/$', views.search),

    # TODO: get from settings
    # url(r'^googlec7fb9df20f08fcee.html', views.google_ver),

    url(r'^i18n/', include(i18n)),

    url(r'^mobile/', views.mobile),
    url(r'^mobile/(?P<firm_id>\d+)$', views.mobile_item),
    url(r'^mobile-search/', views.mobile_search),
    url(r'^mobile-map/', views.mobile_map),

    url(r'^(?P<variable_a>(.+))/(?P<variable_b>(.+))/(?P<variable_c>(.+)).html$', views.v3),
    url(r'^(?P<variable_a>(.+))/(?P<variable_b>(.+))/$', views.v1),
    url(r'^(?P<variable_a>(.+))/$', views.v2),

]

if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ] + urlpatterns
