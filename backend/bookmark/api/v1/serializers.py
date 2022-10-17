from django.http import Http404

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from post.models import Post
from user.models import User
from bookmark.models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class CreateBookmarkSerializer(serializers.ModelSerializer):

    post_id = serializers.IntegerField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data) -> Bookmark:

        bookmarker = validated_data['user']
        post_id = validated_data['post_id']
        try:
            post = (
                Post.objects.filter(id=post_id)
                .select_related('user')
                .only('user__visibility')
                .get()
            )
        except Post.DoesNotExist:
            raise Http404('Post does not exist.')

        if (
            post.user.visibility == User.PUBLIC
            or (post.user_id == bookmarker.id)
            or (bookmarker.is_following(post.user_id))
        ):
            return Bookmark.objects.get_or_create(**validated_data)[0]
        else:
            raise PermissionDenied(
                f'Follow {post.user.username} to bookmark this post.'
            )

    class Meta:
        model = Bookmark
        fields = ('user', 'post_id')
