from datetime import timedelta

from django.contrib import admin
from django.utils import timezone
from django.shortcuts import reverse
from django.db.models import QuerySet
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from story.models import Story


class ActiveStoryFilter(admin.SimpleListFilter):
    title = _('status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', _('Active')),
            ('inactive', _('Inactive')),
        )

    def queryset(self, request, queryset: QuerySet) -> QuerySet:
        duration = timezone.now() - timedelta(days=1)
        match self.value():
            case 'active':
                return (
                    queryset.filter(timestamp__gte=duration)
                    .select_related('user')
                    .only('timestamp', 'user__username')
                )
            case 'inactive':
                return (
                    queryset.filter(timestamp__lt=duration)
                    .select_related('user')
                    .only('timestamp', 'user__username')
                )
            case _:
                return queryset.select_related('user').only(
                    'timestamp',
                    'user__username',
                )


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):

    list_per_page = 50
    ordering = ('-timestamp',)
    list_filter = (ActiveStoryFilter,)
    list_display = ('timestamp', 'poster', 'is_expired')

    def is_expired(self, story: Story) -> bool:
        return story.is_expired

    def poster(self, story: Story) -> str:
        link = reverse('admin:user_user_change', args=[story.user_id])
        return format_html('<a href="{}">{}</a>', link, story.user.username)

    poster.allow_tags = True
    is_expired.boolean = True
