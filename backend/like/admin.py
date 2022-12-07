from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import SafeString

from like.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_filter = ('timestamp',)
    list_display = ('liker', 'post_id', 'timestamp')

    def liker(self, like: Like) -> SafeString:
        link = reverse('admin:user_user_change', args=[like.user.id])
        return format_html('<a href="{}">{}</a>', link, like.user.username)

    def post_id(self, like: Like) -> SafeString:
        link = reverse('admin:post_post_change', args=[like.post_id])
        return format_html('<a href="{}">{}</a>', link, like.post_id)

    post_id.short_description = 'Post'
