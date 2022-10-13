from django.db import models, IntegrityError
from django.contrib.humanize.templatetags import humanize


class Post(models.Model):

    MAX_IMAGES = 5

    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=255, blank=True, default='')
    user = models.ForeignKey(
        'user.User',
        related_name='posts',
        on_delete=models.CASCADE,
    )

    def get_humanized_timestamp(self) -> str:
        return humanize.naturaltime(self.timestamp)

    class Meta:
        ordering = ('-timestamp',)
        indexes: list[models.Index] = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]

    def __str__(self) -> str:
        return str(self.id)


class Image(models.Model):

    file = models.ImageField(upload_to='images/')
    post = models.ForeignKey(
        'post.Post',
        related_name='images',
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        if self.post.images.count() > Post.MAX_IMAGES:
            raise IntegrityError('Post already contains 5 images.')
        else:
            super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.id)
