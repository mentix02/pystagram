from django.db import models


class Like(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        'post.Post',
        related_name='likes',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        'user.User',
        related_name='likes',
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f'{self.user} likes {self.post}'

    class Meta:
        ordering = ('-timestamp',)
        unique_together = ('post', 'user')
