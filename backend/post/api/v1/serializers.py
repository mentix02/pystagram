from rest_framework import serializers

from post.models import Post, Image
from user.api.v1.serializers import ListUserSerializer

IS_LIKED_ANNOTATION = 'is_liked'
LIKE_COUNT_ANNOTATION = 'like_count'
COMMENT_COUNT_ANNOTATION = 'comment_count'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('file',)


class RetrievePostSerializer(serializers.ModelSerializer):

    user = ListUserSerializer()
    images = ImageSerializer(many=True)
    timestamp = serializers.CharField(source='get_humanized_timestamp')

    is_liked = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    # noinspection PyMethodMayBeStatic
    def get_like_count(self, post) -> int:
        return (
            getattr(post, LIKE_COUNT_ANNOTATION)
            if hasattr(post, LIKE_COUNT_ANNOTATION)
            else post.likes.count()
        )

    # noinspection PyMethodMayBeStatic
    def get_comment_count(self, post) -> int:
        return (
            getattr(post, COMMENT_COUNT_ANNOTATION)
            if hasattr(post, COMMENT_COUNT_ANNOTATION)
            else post.comments.count()
        )

    # noinspection PyMethodMayBeStatic
    def get_is_liked(self, post) -> bool:
        if hasattr(post, IS_LIKED_ANNOTATION):
            return getattr(post, IS_LIKED_ANNOTATION)
        else:
            user = self.context['request'].user
            return user.is_authenticated and post.likes.filter(user=user).exists()

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'images',
            'caption',
            'is_liked',
            'timestamp',
            'like_count',
            'comment_count',
        )


class CreatePostSerializer(serializers.ModelSerializer):

    images = ImageSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    caption = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def create(self, validated_data):
        images = self.context['request'].FILES.getlist('images', [])

        if len(images) > Post.MAX_IMAGES:
            raise serializers.ValidationError(
                {'images': [f'You can upload maximum {Post.MAX_IMAGES} images.']}
            )

        if len(images) == 0:
            raise serializers.ValidationError(
                {'images': ['At least one image is required.']}
            )

        post = Post.objects.create(**validated_data)

        for image in images:
            Image.objects.create(post=post, file=image)

        return post

    class Meta:
        model = Post
        fields = ('user', 'caption', 'images')
