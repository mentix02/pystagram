from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView

from post.models import Post
from pystagram.paginators import LargePagination
from post.api.v1.serializers import RetrievePostSerializer
from post.api.v1.utils import generate_annotations, USER_RELATED_DEFERRED_FIELDS
from bookmark.api.v1.serializers import BookmarkSerializer, CreateBookmarkSerializer


class CreateBookmarkAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateBookmarkSerializer


class DeleteBookmarkAPIView(DestroyAPIView):
    lookup_field = "post_id"
    lookup_url_kwarg = "post_id"
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return self.request.user.bookmarks.all()

    def get_object(self):
        post_id = self.request.GET.get("post_id")
        if post_id is None:
            raise ValidationError("post_id is required")
        return get_object_or_404(self.get_queryset(), post_id=post_id)


class ListBookmarkedPostsAPIView(ListAPIView):
    pagination_class = LargePagination
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrievePostSerializer

    def get_queryset(self) -> QuerySet:
        return (
            Post.objects.filter(bookmark__user_id=self.request.user.id)
            .select_related("user")
            .prefetch_related("images")
            .annotate(**generate_annotations(self.request.user))
            .defer(*USER_RELATED_DEFERRED_FIELDS)
            .order_by("-timestamp")
        )
