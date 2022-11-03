from django.db.models import Count, Exists, OuterRef, Expression

from user.models import User
from post.api.v1.serializers import (
    IS_LIKED_ANNOTATION,
    LIKE_COUNT_ANNOTATION,
    COMMENT_COUNT_ANNOTATION,
)


def generate_annotations(request_user: User) -> dict[str, Expression]:

    annotations = {}

    if request_user.is_authenticated:
        annotations[IS_LIKED_ANNOTATION] = Exists(
            request_user.likes.filter(post_id=OuterRef('id'))
        )

    annotations[LIKE_COUNT_ANNOTATION] = Count('likes')
    annotations[COMMENT_COUNT_ANNOTATION] = Count('comments')

    return annotations


USER_RELATED_DEFERRED_FIELDS: list[str] = [
    'user__bio',
    'user__email',
    'user__password',
    'user__is_staff',
    'user__is_active',
    'user__visibility',
    'user__last_login',
    'user__date_joined',
    'user__is_superuser',
]
