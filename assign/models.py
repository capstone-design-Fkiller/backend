from django.db import models

from user.models import User
from apply.models import Apply
from major.models import Major
from locker.models import Locker, Building

class Assign(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="assign", on_delete=models.CASCADE, db_column="user")
    building_id = models.ForeignKey(Building, related_name="assign", on_delete=models.CASCADE, db_column="buidling_id")
    locker = models.ForeignKey(Locker, related_name="assign", on_delete=models.CASCADE, db_column="locker")
    major = models.ForeignKey(Major, related_name="assign", on_delete=models.CASCADE, db_column="major")
    apply = models.ForeignKey(Apply, related_name="assign", on_delete=models.CASCADE, db_column="apply")

    class Meta:
        db_table = "assign"
    
    def __str__(self):
        return str(self.id)

class Unassign(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="unassign", on_delete=models.CASCADE, db_column="user")
    major = models.ForeignKey(Major, related_name="unassign", on_delete=models.CASCADE, db_column="major")
    apply = models.ForeignKey(Apply, related_name="unassign", on_delete=models.CASCADE, db_column="apply")

    class Meta:
        db_table = "unassign"
    
    def __str__(self):
        return str(self.id)