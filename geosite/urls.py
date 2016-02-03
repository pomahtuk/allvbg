from django.conf.urls import url
from django.views.generic import TemplateView

from geosite import views


urlpatterns = [
    url(r'^test/', TemplateView.as_view(template_name="site/test.html")),
    url(r'^firm/add/', views.firm_add),

    url(r'^$', views.print_main_page),
    url(r'^(?P<firm_id>\d+)/$', views.print_page),

    url(r'^main_map.xml', views.map_main_xml),
    url(r'^map.json', views.map_json),
    url(r'^map/(?P<firm_id>\d+).xml', views.map_unmain_xml),

    url(r'^ajax_list/', views.ajax_firm_list),
    url(r'^calend_ajax/', views.calendar_ajax),
    url(r'^events/(?P<event_id>\d+)/$', views.print_event),

    url(r'^about.html', views.about),

    url(r'^contact/send/', views.thank_you),
    url(r'^contact/', views.contact_view),
    url(r'^article/(?P<article_id>\d+)$', views.articles),
    url(r'^search/$', views.search),

    url(r'^mobile/', views.mobile),
    url(r'^mobile/(?P<firm_id>\d+)$', views.mobile_item),
    url(r'^mobile-search/', views.mobile_search),
    url(r'^mobile-map/', views.mobile_map),

    url(r'^(?P<variable_a>(.+))/(?P<variable_b>(.+))/(?P<variable_c>(.+)).html$', views.v3),
    url(r'^(?P<variable_a>(.+))/(?P<variable_b>(.+))/$', views.v1),
    url(r'^(?P<variable_a>(.+))/$', views.v2),
]
