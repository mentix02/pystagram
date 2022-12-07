from django.shortcuts import get_object_or_404

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView

from like.api.v1.serializers import LikeSerializer


class CreateLikeAPIView(CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)


class DeleteLikeAPIView(DestroyAPIView):
    lookup_field = "post_id"
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.likes.all()

    def get_object(self):
        post_id = self.request.GET.get("post_id")
        if post_id is None:
            raise ValidationError("post_id is required")
        return get_object_or_404(self.get_queryset(), post_id=post_id)
