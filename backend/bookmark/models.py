from django.db import models


class Bookmark(models.Model):

    post = models.ForeignKey(
        'post.Post',
        db_index=False,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'user.User',
        related_name='bookmarks',
        on_delete=models.CASCADE,
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} bookmarks {self.post_id}'

    class Meta:
        ordering = ('-timestamp',)
