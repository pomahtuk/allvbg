from django.conf.urls import include, i18n
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.views.static import serve

from geosite import views
from geosite import urls as geosite_urls
from accounts import urls as accounts_urls

from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    url(r'payment/result/$', views.result),
    url(r'payment/pay/$', views.pay),
    url(r'payment/result_ok/$', views.pay_ok),

    # seo part
    url(r'^sitemap.xml', views.sitemap),
    url(r'^rss', views.rss),
    # yandex widget
    url(r'^widget.html', views.widget),


    # TODO: get from settings
    url(r'^googlec7fb9df20f08fcee.html', TemplateView.as_view(template_name="agenda/google.html")),


    url(r'^i18n/', include(i18n)),
    url(r'^', include(accounts_urls)),
    url(r'^', include(geosite_urls))

]

if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ] + urlpatterns
