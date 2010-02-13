# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sites.models import Site


def index(request):
    return render_to_response('test_app/index.html', {}, context_instance=RequestContext(request))

def counter(request):
    return render_to_response('test_app/counter.html', {
                                'guinea_pig': Site.objects.get_current(),
                                'url': "http://%s" % Site.objects.get_current().domain
                              },
                              context_instance=RequestContext(request))
