from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html


from bookmark.models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):

    list_filter = ('timestamp',)
    list_display = ('bookmarker', 'post', 'timestamp')

    def bookmarker(self, bookmark):
        link = reverse('admin:user_user_change', args=[bookmark.user_id])
        return format_html('<a href="{}">{}</a>', link, bookmark.user.username)

    bookmarker.short_description = 'Bookmarker'
