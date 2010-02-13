from django.conf.urls.defaults import *

from test_app.views import index, counter

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^counter/$', counter, name='counter'),
)