from django.http import Http404

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from like.models import Like
from post.models import Post
from user.models import User


class LikeSerializer(serializers.ModelSerializer):

    post_id = serializers.IntegerField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data) -> Like:

        # if owner of post has public profile, then create like
        # else, check if logged-in user is in the list of followers

        liker = validated_data['user']
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
            or (post.user_id == liker.id)
            or (liker.is_following(post.user_id))
        ):
            return Like.objects.get_or_create(**validated_data)[0]
        else:
            raise PermissionDenied(f'Follow {post.user.username} to like this post.')

    class Meta:
        model = Like
        fields = ('user', 'post_id')
