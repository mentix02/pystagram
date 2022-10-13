from django.db.models import QuerySet

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView

from comment.models import Comment
from pystagram.paginators import LargePagination
from comment.api.v1.serializers import CommentSerializer, CreateCommentSerializer


class CreateCommentAPIView(CreateAPIView):

    queryset = Comment.objects.none()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCommentSerializer


class ListPostCommentAPIView(ListAPIView):

    pagination_class = LargePagination
    serializer_class = CommentSerializer

    def get_queryset(self) -> QuerySet:
        return Comment.objects.filter(post_id=self.kwargs['post_id'])


class DeleteCommentAPIView(DestroyAPIView):

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return Comment.objects.filter(user_id=self.request.user.id)
