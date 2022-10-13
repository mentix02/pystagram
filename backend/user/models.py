from __future__ import annotations

import typing

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractUser,
    UserManager as AbstractUserManager,
)

from feed.models import FollowRequest


class UserManager(AbstractUserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractUser):

    PRIVATE = True
    PUBLIC = False

    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )

    email = models.EmailField(_('email address'), unique=True)
    bio = models.CharField(max_length=255, blank=True, default='')
    visibility = models.BooleanField(default=PUBLIC, choices=VISIBILITY_CHOICES)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/', blank=True)

    _follows = models.ManyToManyField('User', blank=True, related_name='followed_by')

    objects = UserManager()

    def follow(
        self,
        user: User,
        force: bool = False,
    ) -> typing.Union[FollowRequest, bool]:
        if user.id == self.id:
            return False

        if self.following.filter(id=user.id).exists():
            return False

        if force:
            self._follows.add(user)
            return True

        if user.visibility == self.PRIVATE:
            request, _ = FollowRequest.objects.get_or_create(
                requester=self,
                to_follow=user,
            )
            return request
        else:
            self._follows.add(user)
            return True

    def unfollow(self, user: User):
        self._follows.remove(user)

    def is_following(self, user_or_id: typing.Union[User, int]) -> bool:
        if isinstance(user_or_id, User):
            user_id = user_or_id.id
        else:
            user_id = user_or_id
        return self.following.filter(id=user_id).exists()

    def is_followed_by(self, user_or_id: typing.Union[User, int]) -> bool:
        if isinstance(user_or_id, User):
            user_id = user_or_id.id
        else:
            user_id = user_or_id
        return self.followers.filter(id=user_id).exists()

    @property
    def following(self) -> models.QuerySet:
        """Returns a QuerySet of Users that this user follows."""
        return self._follows.all()

    @property
    def followers(self) -> models.QuerySet:
        """Returns a QuerySet of Users following this user."""
        return self.followed_by.all()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.username = self.username.lower()
        super().save(*args, **kwargs)
