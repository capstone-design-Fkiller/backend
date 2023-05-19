from django.db import models

from major.models import Major
from user.models import User

class Alert(models.Model):
    id = models.BigAutoField(primary_key=True)
    major = models.ForeignKey(Major, related_name="alert", on_delete=models.PROTECT, db_column="major")
    message = models.CharField(max_length=200)
    sender = models.ForeignKey(User, related_name="alert_sender", on_delete=models.PROTECT, db_column="sender")
    receiver = models.ForeignKey(User, related_name="alert_receiver", on_delete=models.PROTECT, db_column="receiver")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)