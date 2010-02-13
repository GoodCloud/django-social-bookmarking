import urlparse

from django.template import Library
from django.utils.http import urlquote
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from social_bookmarking.models import Bookmark, BookmarkRelated, DEFAULT_VISITS

register = Library()

class NoRequestContextProcessorFound(Exception):
    pass

@register.inclusion_tag('social_bookmarking/links.html', takes_context=True)
def show_bookmarks(context, title, object_or_url, description=""):
    """
    Displays the bookmarks
    TODO: Add in the javascript cleanup part
    """

    if hasattr(object_or_url, 'get_absolute_url'):
        url = getattr(object_or_url, 'get_absolute_url')()

    url = unicode(object_or_url)
    
    if not url.startswith('http'):
        url = context['request'].build_absolute_uri(url)

    # TODO: Bookmark should have a .active manager:
    bookmarks = Bookmark.objects.get_active().values()

    for bookmark in bookmarks:
        bookmark['description'] = description
        bookmark['link'] = bookmark['url'] % {'title': urlquote(title),
                                        'url': urlquote(url),
                                        'description': urlquote(description)
                                       }


    return {'bookmarks':bookmarks, 'MEDIA_URL': context['MEDIA_URL']}

@register.inclusion_tag('social_bookmarking/links_related.html', takes_context=True)
def show_bookmarks_related(context, title, url, object, description=""):
    """
    Displays the bookmarks with counter.
    """
    
    if not isinstance(object, models.Model):
        raise TypeError, "object must be a valid Model"
    
    bookmarks = Bookmark.objects.get_active().values()
    content_type = ContentType.objects.get_for_model(object)
    bookmarks_related = dict((related['bookmark_id'], related)\
                             for related in BookmarkRelated.objects.filter(content_type=content_type,
                                                                           object_id=object.pk)
                                                                   .values())
    
    for bookmark in bookmarks:
        bookmark.update({
            'url': urlquote(bookmark['url'] % {'title': urlquote(title),
                                      'url': urlquote(url),
                                      'description': urlquote(description)}),
            'content_type': "%s.%s" % (content_type.app_label, content_type.model),
            'object_pk': object.pk,
            'visits': bookmarks_related[bookmark['id']]['visits'] if bookmark['id'] in bookmarks_related else DEFAULT_VISITS
        })
    
    return {'bookmarks': bookmarks, 'MEDIA_URL': context['MEDIA_URL']}

