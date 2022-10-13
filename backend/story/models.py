from datetime import timedelta

from django.db import models
from django.utils import timezone


class Story(models.Model):

    image = models.ImageField(upload_to='stories/')
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'user.User',
        related_name='stories',
        on_delete=models.CASCADE,
    )

    @property
    def is_expired(self) -> bool:
        return timezone.now() - self.timestamp > timedelta(days=1)

    def __str__(self) -> str:
        return f'{self.user} - {self.timestamp}'

    class Meta:
        ordering = ('-timestamp',)
        verbose_name_plural = 'stories'
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]
