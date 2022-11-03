from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveDestroyAPIView,
)

from user.models import User
from post.api.v1.utils import (
    generate_annotations,
    USER_RELATED_DEFERRED_FIELDS,
)
from post.api.v1.serializers import (
    CreatePostSerializer,
    RetrievePostSerializer,
)


class CreatePostAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreatePostSerializer


class DestroyPostAPIView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrievePostSerializer

    def get_queryset(self):
        return self.request.user.posts.all()


class ListUserPostAPIView(ListAPIView):
    serializer_class = RetrievePostSerializer

    def get_queryset(self):
        request_user = self.request.user
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)

        if (
            user.visibility == User.PUBLIC
            or (request_user.is_authenticated and request_user == user)
            or (request_user.is_authenticated and request_user.is_following(user))
        ):
            deferred_fields = USER_RELATED_DEFERRED_FIELDS
            annotations = generate_annotations(request_user)
            return (
                user.posts.select_related('user')
                .prefetch_related('images')
                .annotate(**annotations)
                .defer(*deferred_fields)
                .order_by('-timestamp')
            )
        else:
            raise PermissionDenied(f'Follow {user.username} to see their posts.')
