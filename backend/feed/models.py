from django.db import models


class FollowRequest(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)

    requester = models.ForeignKey(
        'user.User',
        db_index=False,
        related_name='+',
        on_delete=models.CASCADE,
    )

    to_follow = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='follow_requests',
    )

    def reject(self):
        self.delete()

    def accept(self):
        self.requester.follow(self.to_follow, force=True)
        self.delete()

    def __str__(self) -> str:
        return f'{self.requester} -> {self.to_follow}'

    class Meta:
        ordering = ('-timestamp',)
        unique_together = ('requester', 'to_follow')
