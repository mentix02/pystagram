from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView

from user.models import User
from post.models import Post
from post.api.v1.serializers import RetrievePostSerializer
from post.api.v1.utils import generate_annotations, USER_RELATED_DEFERRED_FIELDS
from feed.api.v1.serializers import (
    FollowUserSerializer,
    UnfollowUserSerializer,
    FollowRequestSerializer,
)


class FeedAPIView(ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = RetrievePostSerializer

    def get_queryset(self) -> QuerySet:

        user = self.request.user

        annotations = generate_annotations(user)
        deferred_fields = USER_RELATED_DEFERRED_FIELDS

        following = user.following
        following_ids = list(following.values_list('id', flat=True)) + [user.id]

        return (
            Post.objects.filter(user__id__in=following_ids)
            .select_related('user')
            .prefetch_related('images')
            .annotate(**annotations)
            .defer(*deferred_fields)
            .order_by('-timestamp')
        )


class ListFollowRequestAPIView(ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = FollowRequestSerializer

    def get_queryset(self) -> QuerySet:
        return self.request.user.follow_requests.all()


class FollowUserAPIView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = FollowUserSerializer


class UnfollowUserAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request: Request) -> Response:
        user: User = request.user
        serializer = UnfollowUserSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        to_unfollow_id: int = serializer.validated_data['to_unfollow_id']
        user.unfollow(get_object_or_404(User, id=to_unfollow_id))

        return Response({'unfollowed': True})
