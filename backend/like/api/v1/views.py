from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView

from like.api.v1.serializers import LikeSerializer


class CreateLikeAPIView(CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)


class DeleteLikeAPIView(DestroyAPIView):
    lookup_field = 'post_id'
    lookup_url_kwarg = 'post_id'
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.likes.all()
