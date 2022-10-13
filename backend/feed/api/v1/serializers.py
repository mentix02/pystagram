from django.shortcuts import get_object_or_404

from rest_framework import serializers

from user.models import User
from feed.models import FollowRequest
from user.api.v1.serializers import ListUserSerializer


class FollowRequestSerializer(serializers.ModelSerializer):

    requester = ListUserSerializer()

    class Meta:
        model = FollowRequest
        fields = ('requester', 'timestamp')


class FollowUserSerializer(serializers.Serializer):

    followed = serializers.BooleanField(read_only=True)
    requested = serializers.BooleanField(read_only=True)
    follower = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_follow_id = serializers.IntegerField(required=True, write_only=True, min_value=1)

    def validate_to_follow_id(self, value):
        if value == self.context['request'].user.id:
            raise serializers.ValidationError('You cannot follow yourself.')

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError('User does not exist.')

        return value

    def create(self, validated_data):
        follower: User = validated_data['follower']
        to_follow_id: int = validated_data['to_follow_id']

        result = follower.follow(get_object_or_404(User, id=to_follow_id))

        if result is True:
            return {'followed': True, 'requested': False}
        elif isinstance(result, FollowRequest):
            return {'followed': False, 'requested': True}
        else:
            return {'followed': False, 'requested': False}


class UnfollowUserSerializer(serializers.Serializer):

    to_unfollow_id = serializers.IntegerField(
        required=True, write_only=True, min_value=1
    )

    def validate_to_unfollow_id(self, value):
        if value == self.context['request'].user.id:
            raise serializers.ValidationError('You cannot unfollow yourself.')

        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError('User does not exist.')

        return value
