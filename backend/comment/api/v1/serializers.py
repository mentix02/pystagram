from rest_framework import serializers

from comment.models import Comment
from user.api.v1.serializers import ListUserSerializer


class CommentSerializer(serializers.ModelSerializer):

    user = ListUserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CreateCommentSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
