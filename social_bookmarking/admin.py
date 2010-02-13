from django.contrib import admin
from social_bookmarking.models import Bookmark, BookmarkRelated

class BookmarkAdmin(admin.ModelAdmin):
    list_display    = ('title', 'status')
    list_filter     = ('title', 'status')
    search_fields   = ('title', 'status')
    list_editable   = ('status',)

class BookmarkRelatedAdmin(admin.ModelAdmin):
    list_display    = ('content_type', 'object_id', 'visits', 'bookmark')
    list_filter     = ('content_type', )

admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(BookmarkRelated, BookmarkRelatedAdmin)

