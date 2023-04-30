from django.db import models

from major.models import Major
from user.models import User

class Building(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20) # ex) 1 - 인문관, 3 - 사회과학관


class Locker(models.Model):
    id = models.BigAutoField(primary_key=True)
    building_id = models.IntegerField()
    # building_id = models.ForeignKey(Building, related_name='locker', on_delete=models.PROTECT, db_column='building_id')
    major = models.ForeignKey(Major, related_name="locker", on_delete=models.PROTECT, db_column="major")
    owned_id = models.ForeignKey(User, related_name='owned_locker', on_delete=models.PROTECT, db_column="owned_id", null=True, blank=True)
    shared_id = models.ForeignKey(User, related_name='shared_locker', on_delete=models.PROTECT, db_column="shared_id", null=True, blank=True)
    is_share_registered = models.BooleanField(default=False) # 쉐어를 하겠다고 등록한 경우
    start_date = models.DateTimeField(null=True, blank=True) # 학과 대여 시작 날짜, 이름 헷갈리나?
    end_date = models.DateTimeField(null=True, blank=True) # 학과 대여 종료 날짜
    share_start_date = models.DateTimeField(null=True, blank=True) # 유저간 쉐어 시작 날짜
    share_end_date = models.DateTimeField(null=True, blank=True) # 유저간 쉐어 종료 날짜