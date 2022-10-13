from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from django.db.models import QuerySet

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView

from user.models import User
from story.models import Story
from user.api.v1.serializers import ListUserSerializer
from story.api.v1.utils import generate_deferred_fields
from story.api.v1.serializers import CreateStorySerializer, RetrieveStorySerializer


class CreateStoryAPIView(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = CreateStorySerializer


class ListFollowingWithActiveStories(ListAPIView):

    serializer_class = ListUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        duration = timezone.now() - timedelta(days=1)
        following_ids = [user.id] + list(user.following.values_list('id', flat=True))
        return (
            User.objects.filter(
                id__in=following_ids,
                stories__timestamp__gte=duration,
            )
            .only(*ListUserSerializer.Meta.fields)
            .distinct()
        )


class ListActiveStoriesFeedAPIView(ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = RetrieveStorySerializer

    def get_queryset(self) -> QuerySet:
        return (
            Story.objects.filter(
                timestamp__gte=timezone.now() - timedelta(days=1),
                user_id__in=self.request.user.following.values_list('id', flat=True),
            )
            .select_related('user')
            .defer(*generate_deferred_fields())
            .order_by('user_id', '-timestamp')
        )


class ListActiveStoriesAPIView(ListAPIView):

    serializer_class = RetrieveStorySerializer

    def get_queryset(self) -> QuerySet:
        """gets stories posted by a user in the last 24 hours"""
        username = self.kwargs['username']
        request_user: User = self.request.user
        try:
            user = (
                User.objects.filter(username=username).only('id', 'visibility').first()
            )
        except User.DoesNotExist:
            raise Http404(f'User "{username}" not found.')

        if (
            user.visibility == User.PUBLIC
            or (request_user.is_authenticated and request_user.id == user.id)
            or (request_user.is_authenticated and request_user.is_following(user.id))
        ):
            return (
                Story.objects.filter(
                    user_id=user,
                    timestamp__gte=timezone.now() - timedelta(days=1),
                )
                .select_related('user')
                .defer(*generate_deferred_fields())
                .order_by('-timestamp')
            )
        else:
            raise PermissionDenied(f'Follow {user.username} to see their stories.')
