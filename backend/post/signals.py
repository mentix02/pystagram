from django.db import IntegrityError
from django.dispatch import receiver
from django.db.models.signals import pre_delete

from post.models import Image


# noinspection PyUnusedLocal
@receiver(pre_delete, sender=Image)
def create_auth_token(sender, instance: Image, **kwargs):
    # prevent if post has only 1 image left
    if Image.objects.filter(post_id=instance.post_id).count() == 1:
        raise IntegrityError('Post must have at least 1 image.')
