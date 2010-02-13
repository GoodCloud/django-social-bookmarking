from django.conf.urls.defaults import *
from django.forms.fields import url_re

from social_bookmarking.views import bookmark_referer

urlpatterns = patterns('', 
    url(r'^referer/(?P<slug>[-\w]+)/(?P<content_type>[\.\w]+)/(?P<object_pk>[\d]+)/(?P<url>.*)$',
        bookmark_referer,
        name='bookmark_referer'),
)