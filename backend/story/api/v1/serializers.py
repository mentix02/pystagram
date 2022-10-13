from rest_framework import serializers

from story.models import Story
from user.api.v1.serializers import ListUserSerializer


class RetrieveStorySerializer(serializers.ModelSerializer):

    user = ListUserSerializer()
    timestamp = serializers.DateTimeField(format='%b %d, %Y %I:%M %p')

    class Meta:
        model = Story
        fields = ('image', 'timestamp', 'user')


class CreateStorySerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Story
        fields = ('image', 'user')
