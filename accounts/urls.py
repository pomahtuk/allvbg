from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login

import views


urlpatterns = [
    url(r'^accounts/login/$', login, {'template_name': 'site/login.html'}),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/profile/$', views.profile_view),
    url(r'^accounts/profile/edit/$', views.manage_user_profile),
    url(r'^accounts/profile/firm/$', views.manage_firm),
    url(r'^accounts/edit/firm/(?P<firm_id>\d+)/$', views.profile_edit_firm),
    url(r'^accounts/profile/(?P<user_id>\d+)/$', views.profile_view_id),
]