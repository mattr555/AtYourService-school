from django.conf.urls import patterns, url
from main import views, user_views, org_views, nhs_views, endpoints

urlpatterns = patterns('',
    # user management
    url(r'^login/$', user_views.login_view, name='login'),
    url(r'^logout/', user_views.logout_view, name='logout'),
    url(r'^signup/', user_views.signup, name='signup'),
    url(r'^profile/change_loc/$', user_views.change_location, name='change_loc'),
    url(r'^profile/reset_pass/complete/$', user_views.finish_change_pass),
    url(r'^profile/change_pass/complete/$', user_views.finish_change_pass),
    url(r'^profile/$', user_views.user_profile, name='user_profile'),
    url(r'^profile/email_validation/(?P<key>[a-zA-Z]{20})/$', user_views.email_validation, name='email_validation'),

    # organization management
    url(r'^manage/$', org_views.manage_home, name='manage_home'),
    url(r'^manage/org/(?P<pk>\d+)/$', org_views.org_home, name='org_home'),
    url(r'^manage/org/(?P<pk>\d+)/edit/$', org_views.org_edit, name='org_edit'),
    url(r'^manage/org/new/$', org_views.org_new, name='org_create'),
    url(r'^manage/org/(?P<pk>\d+)/delete/$', org_views.org_delete, name='org_delete'),
    url(r'^manage/event/(?P<pk>\d+)/$', org_views.event_home, name='event_home'),
    url(r'^manage/event/(?P<pk>\d+)/edit/$', org_views.event_edit, name='event_edit'),
    url(r'^manage/event/new/$', org_views.event_new, name='event_create'),
    url(r'^manage/event/(?P<pk>\d+)/delete/$', org_views.event_delete, name='event_delete'),

    #NHS management
    url(r'^nhs/$', nhs_views.nhs_home, name='nhs_home'),
    url(r'^nhs/list/candidates/$', nhs_views.nhs_candidate_list, name='nhs_candidate_list'),
    url(r'^nhs/list/members/$', nhs_views.nhs_member_list, name='nhs_member_list'),
    url(r'^nhs/settings/$', nhs_views.nhs_settings, name='nhs_settings'),
    url(r'^nhs/user/(?P<pk>\d+)/$', nhs_views.nhs_user_report, name='nhs_user_report'),
    url(r'^nhs/user/(?P<pk>\d+)/org_admin/$', nhs_views.change_org_admin, name='change_org_admin'),
    url(r'^nhs/user/(?P<pk>\d+)/demerit/$', nhs_views.demerit, name='nhs_demerit'),
    url(r'^nhs/demerit/(?P<pk>\d+)/delete/$', nhs_views.delete_demerit, name='nhs_delete_demerit'),
    url(r'^nhs/user/(?P<pk>\d+)/induct/$', nhs_views.induct, name='nhs_induct'),

    url(r'^forbidden/$', views.forbidden),

    #ajax
    url(r'^ajax/main/do_event.json', endpoints.do_event),
    url(r'^ajax/main/dont_do_event.json', endpoints.dont_do_event),
    url(r'^ajax/main/join_org.json', endpoints.join_org),
    url(r'^ajax/main/unjoin_org.json', endpoints.unjoin_org),
    url(r'^ajax/main/confirm_participant.json', endpoints.confirm_participant),
    url(r'^ajax/main/unconfirm_participant.json', endpoints.unconfirm_participant),
    url(r'^ajax/main/username_valid.json', endpoints.username_valid),
    url(r'^ajax/main/toggle_event_approval.json', endpoints.toggle_event_approval),

    url(r'^list/(?P<page>\d+)/', views.list_events, name='list_page'),
    url(r'^list/$', views.list_events_one, name='list_events'),
    url(r'^event/(?P<pk>\d+)/', views.EventView.as_view(), name='event_detail'),
    url(r'^userevent/(?P<pk>\d+)/$', views.userevent_detail, name='userevent_detail'),
    url(r'^userevent/(?P<pk>\d+)/delete/', views.delete_userevent, name='userevent_delete'),
    url(r'^organization/(?P<pk>\d+)/', views.organization_detail, name='organization_detail'),
    url(r'^track/', views.track_events, name='track'),
    url(r'^$', views.home, name='home'),
)
