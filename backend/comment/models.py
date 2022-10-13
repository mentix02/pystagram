from django.db import models


class Comment(models.Model):

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        'post.Post',
        related_name='comments',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        'user.User',
        related_name='comments',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self) -> str:
        return self.content[:25]
