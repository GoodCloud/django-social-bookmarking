from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from social_bookmarking.models import BookmarkRelated, Bookmark

def bookmark_referer(request, slug, content_type, object_pk, url):
    """
        Redirect to bookmark url if content_type exists
        and object related exists too.
        If there is no error, the related bookmark counter is incremented.
    """
    bookmark = get_object_or_404(Bookmark, slug=slug)
    
    app, model = content_type.split('.')
    try:
        ctype = ContentType.objects.get(app_label=app, model=model)
        content_object = ctype.get_object_for_this_type(pk=object_pk)
    except ObjectDoesNotExist:
        raise Http404
    
    related, is_created = BookmarkRelated.objects.get_or_create(content_type=ctype,
                                                    object_id=content_object.pk,
                                                    bookmark=bookmark)
    related.visits += 1
    related.save()
    
    return redirect(url)