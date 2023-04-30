from django.db import models

from major.models import Major
from user.models import User

#Create your models here.

class Locker(models.Model): # 얘 만들려면 major db가 먼저 있어야 한다.
    id = models.BigAutoField(primary_key=True)
    building_id = models.IntegerField() # 빌딩은 int로 잘 되었고,
    major = models.ForeignKey(Major, related_name="locker", on_delete=models.PROTECT, db_column="major") # 맞는지 모르겠다.
    owned_id = models.ForeignKey(User, related_name='owned_locker', on_delete=models.PROTECT, db_column="owned_id", null=True, blank=True) # 이건 맞고 
    shared_id = models.ForeignKey(User, related_name='shared_locker', on_delete=models.PROTECT, db_column="shared_id", null=True, blank=True) # 이것도 맞다.
    is_share_registered = models.BooleanField(default=False) # 쉐어를 하겠다고 등록한 경우
    start_date = models.DateTimeField(null=True, blank=True) # 대여 시작 날짜, 대여라는 이름을 붙여야겠다. 이름 헷갈린다.
    end_date = models.DateTimeField(null=True, blank=True) # 대여 종료 날짜, 대여라는 이름을 붙여야겠다. 이름 헷갈린다.
    share_start_date = models.DateTimeField(null=True, blank=True) # 쉐어 시작 날짜
    share_end_date = models.DateTimeField(null=True, blank=True) # 쉐어 종료 날짜

    class Meta:
        db_table = 'locker'

    def __str__(self):
        return self.name