from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from rest_framework.authtoken.models import Token

from user.models import User
from bookmark.models import Bookmark


# noinspection PyUnusedLocal
@receiver(post_save, sender=User)
def create_auth_token(sender, instance: User = None, created: bool = False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# noinspection PyUnusedLocal
@receiver(m2m_changed, sender=User._follows.through)
def delete_bookmarks(sender, instance: User = None, action=None, pk_set=None, **kwargs):
    if action == 'post_remove':
        Bookmark.objects.filter(user=instance, post__user_id__in=pk_set).delete()
