from django.shortcuts import get_object_or_404

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
        post = get_object_or_404(Post, id=post_id)

        if post.user.visibility == User.PUBLIC or liker.is_following(post.user):
            return Like.objects.get_or_create(**validated_data)[0]
        else:
            raise PermissionDenied(f'Follow {post.user.username} to like this post.')

    class Meta:
        model = Like
        fields = ('user', 'post_id')
