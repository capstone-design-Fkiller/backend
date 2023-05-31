from django.db import models

from major.models import Major
from user.models import User

# ----건물번호----
# 교내에서 사용하는 건물번호를 그대로 적용, 사이버관은 원래 C로 표현하는데 임의로 5로 지정
# 인문과학관 : 1, 교수학습개발원 : 2, 사회과학관 : 3, 국제학사 : 4, 사이버관 : 5
class Building(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'building'

    def __str__(self):
        return self.name

#Create your models here.
class Locker(models.Model):
    id = models.BigAutoField(primary_key=True)
    major = models.ForeignKey(Major, related_name="locker", on_delete=models.PROTECT, db_column="major")
    floor = models.CharField(max_length=10)
    building_id = models.ForeignKey(Building, related_name='locker', on_delete=models.PROTECT, db_column='building_id')
    owned_id = models.ForeignKey(User, related_name='owned_locker', on_delete=models.PROTECT, db_column="owned_id", null=True, blank=True) 
    shared_id = models.ForeignKey(User, related_name='shared_locker', on_delete=models.PROTECT, db_column="shared_id", null=True, blank=True)
    is_share_registered = models.BooleanField(default=False) # 쉐어를 하겠다고 등록한 경우
    share_start_date = models.DateTimeField(null=True, blank=True) # 유저간 쉐어 시작 날짜
    share_end_date = models.DateTimeField(null=True, blank=True) # 유저간 쉐어 종료 날짜
    start_date = models.ForeignKey(Major, related_name='locker_start_date', on_delete=models.PROTECT, db_column="start_date", null=True, blank=True) # 학과 배정 시작 ㄱ날짜
    end_date = models.ForeignKey(Major, related_name='locker_end_date', on_delete=models.PROTECT, db_column="end_date", null=True, blank=True) # 학과 배정 종료 날짜

    class Meta:
        db_table = 'locker'

    def __str__(self):
        return str(self.id)
