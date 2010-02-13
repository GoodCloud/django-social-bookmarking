from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root),
    url(r'^social/', include('social_bookmarking.urls')),
    url(r'^', include('test_app.urls', namespace='test')),
)
