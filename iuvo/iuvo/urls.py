from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
# from iuvo_app.forms import RegisterForm
# import iuvo_app.urls
# from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('iuvo_app.urls')),
                       url(r'^accounts/',
                           include('allauth.urls')),
                       )
