from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html


from like.models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_filter = ('timestamp',)
    list_display = ('liker', 'post', 'timestamp')

    def liker(self, like):
        link = reverse('admin:user_user_change', args=[like.user.id])
        return format_html('<a href="{}">{}</a>', link, like.user.username)
