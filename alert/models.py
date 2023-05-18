from django.db import models

from major.models import Major
from user.models import User

class Alert(models.Model):
    id = models.BigAutoField(primary_key=True)
    major = models.ForeignKey(Major, related_name="alert", on_delete=models.PROTECT, db_column="major")
    message = models.CharField(max_length=200, require=True)
    sender = models.ForeignKey(User, related_name="alert", on_delete=models.PROTECT, db_column="user")
    receiver = models.ForeignKey(User, related_name="alert", on_delete=models.PROTECT, db_column="user")
    created_at = models.DateTimeField(auto_now_add=True)