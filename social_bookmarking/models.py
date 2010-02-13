from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.http import urlquote
from django.utils.translation import ugettext as _

DEFAULT_VISITS = 0

STATUS_CHOICES = (
    (1, 'Inactive'),
    (2, 'Active'),
)

url_help = """
Not a formal URL field. This accepts a string which will have string formatting operations performed on it. Valid key 
mappings for the string formatting includes:
<ul>
  <li><strong>%(url)s</strong> Url to be provided to social bookmarking service</li>
  <li><strong>%(title)s</strong> Title of object being submitted to social bookmarking service</li>  
  <li><strong>%(description)s</strong> Summary or description of the object being submitted</li>    
</ul>
"""

image_help = """
Bookmark image icon stored in media/social_bookmarking/img folder. Stored there so easier to install with fixtures."
"""

js_help = """
Javascript placed here will be inserted in the page in a <script></script> body. Lines will be stripped so make sure that 
you end your lines of code correctly.
"""

class BookmarkManager(models.Manager):
    """
    QuerySet for all acive bookmarks.
    """
    def get_active(self):
        return self.get_query_set().filter(status=2)

class Bookmark(models.Model):
    title           = models.CharField(max_length=255, blank=False)
    slug            = models.SlugField(_('slug'))
    status          = models.IntegerField(choices=STATUS_CHOICES, default=2)    
    description     = models.CharField(max_length=255, blank=True, help_text=_("Because some things want it"))
    url             = models.CharField(blank=False, max_length=255, help_text=_(url_help))
    image           = models.CharField(help_text=_(image_help), max_length=100, blank=False)
    js              = models.TextField(help_text=_(js_help), blank=True)
    
    objects = BookmarkManager()
    
    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return unicode(self.title)

class BookmarkRelated(models.Model):
    content_type    = models.ForeignKey(ContentType)
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey('content_type', 'object_id')
    bookmark        = models.ForeignKey(Bookmark, blank=False, null=False)
    visits          = models.IntegerField(_('visits'), default=DEFAULT_VISITS, editable=False)