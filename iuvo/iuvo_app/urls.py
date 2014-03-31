from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    'iuvo_app.views',
    url(r'^$', 'home_view', name='home'),
    url(r'^login/$', 'login_view', name='login'),
    url(r'^register/$', 'register_view', name='register'),
    url(r'^about/$', 'about_view', name='about'),

    url(r'^(\d+)/$', 'dashboard_view', name='dashboard'),
    url(r'^(\d+)/events/(\d+)/checkin/$', 'dashboard_view', name='dashboard'),

    url(r'^(\d+)/events/new/$', 'create_event_view', name='create_event'),
    url(r'^(\d+)/events/(\d+)/$', 'view_event_view', name='view_event'),
    url(r'^(\d+)/events/(\d+)/edit/$', 'edit_event_view', name='edit_event'),

    url(r'^(\d+)/events/$', 'events_list_view', name='events_list'),
    url(r'^(\d+)/events/upcoming/$', 'events_upcoming_view', name='events_upcoming'),
    url(r'^(\d+)/events/current/$', 'events_current_view', name='events_current'),
    url(r'^(\d+)/events/past/$', 'events_past_view', name='events_past'),

    url(r'^(\d+)/contacts/new/$', 'create_contact_view', name='create_contact'),
    url(r'^(\d+)/contacts/(\d+)/$', 'view_contact_view', name='view_contact'),
    url(r'^(\d+)/contacts/(\d+)/edit/$', 'edit_contact_view', name='edit_contact'),
    url(r'^(\d+)/contacts/$', 'contacts_list_view', name='contacts_list'),
)
