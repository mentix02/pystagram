import typing

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError

from user.models import User
from user.api.v1.serializers import (
    ListUserSerializer,
    CreateUserSerializer,
    ObtainAuthDataSerializer,
)


class UsernameAvailabilityAPIView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        username: str = request.GET.get('username', '')
        if username == '':
            raise ValidationError({'username': ['This field is required.']})
        return Response(
            {
                'available': not User.objects.filter(
                    username__iexact=username.strip()
                ).exists()
            }
        )


class ObtainAuthDataAPIView(CreateAPIView):

    queryset = User.objects.none()
    serializer_class = ObtainAuthDataSerializer


class CreateUserAPIView(CreateAPIView):

    queryset = User.objects.none()
    serializer_class = CreateUserSerializer


def user_relation_list_view_factory(relation_attr: str) -> typing.Type[ListAPIView]:
    class UserRelationListView(ListAPIView):
        serializer_class = ListUserSerializer
        permission_classes = (IsAuthenticated,)

        def get_queryset(self):
            username = self.kwargs['username']
            user = get_object_or_404(User, username=username)

            if (
                user.visibility == User.PUBLIC
                or user.id == self.request.user.id
                or self.request.user.is_following(user)
            ):
                return getattr(user, relation_attr).all()
            else:
                raise PermissionDenied(
                    f'Follow {user.username} to see their {relation_attr}.'
                )

    return UserRelationListView


UserFollowingAPIView = user_relation_list_view_factory('following')
UserFollowersAPIView = user_relation_list_view_factory('followers')
