from django import forms
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars

from post.models import Post, Image


class ImageAdminInline(admin.StackedInline):
    extra = 0
    min_num = 1
    model = Image
    max_num = Post.MAX_IMAGES


class PostAdminForm(forms.ModelForm):

    caption = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    form = PostAdminForm
    inlines = [ImageAdminInline]
    list_filter = ('timestamp',)
    list_display_links = ('id', 'caption')
    list_display = ('id', 'caption', 'poster', 'num_likes', 'timestamp')

    def num_likes(self, post):
        return post.likes.count()

    def caption(self, post):
        return truncatechars(post.caption, 15)

    def poster(self, post):
        link = reverse('admin:user_user_change', args=[post.user.id])
        return format_html('<a href="{}">{}</a>', link, post.user.username)

    poster.allow_tags = True
    caption.short_description = 'Caption'
    num_likes.short_description = 'Likes'
