from django.db import models

from major.models import Major
from user.models import User


class Notice(models.Model):
    id = models.BigAutoField(primary_key=True)
    major = models.ForeignKey(Major, related_name="notice", on_delete=models.PROTECT, db_column="major")
    title = models.CharField(max_length=200)
    content = models.TextField()
    writer = models.ForeignKey(User, related_name="notice_sender", on_delete=models.PROTECT, db_column="sender")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)