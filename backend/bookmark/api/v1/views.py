from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView

from post.models import Post
from pystagram.paginators import LargePagination
from post.api.v1.serializers import RetrievePostSerializer
from post.api.v1.utils import generate_annotations, generate_deferred_fields
from bookmark.api.v1.serializers import BookmarkSerializer, CreateBookmarkSerializer


class CreateBookmarkAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateBookmarkSerializer


class DeleteBookmarkAPIView(DestroyAPIView):
    lookup_field = 'post_id'
    lookup_url_kwarg = 'post_id'
    serializer_class = BookmarkSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return self.request.user.bookmarks.all()


class ListBookmarkedPostsAPIView(ListAPIView):
    pagination_class = LargePagination
    permission_classes = (IsAuthenticated,)
    serializer_class = RetrievePostSerializer

    def get_queryset(self) -> QuerySet:
        return (
            Post.objects.filter(bookmark__user_id=self.request.user.id)
            .select_related('user')
            .prefetch_related('images')
            .annotate(**generate_annotations(self.request.user))
            .defer(*generate_deferred_fields())
            .order_by('-timestamp')
        )
