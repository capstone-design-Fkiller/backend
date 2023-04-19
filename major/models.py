from django.db import models

# Create your models here.

class Major(models.Model): # 관리자들이 설정하는 학과 정보
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100) #학과명, 근데 이거는 학과명이 고유한 값으로 검색이 되어야 하는데, id로 하려면, 학과마다 번호를 붙여야할 수도 있겠다. 얘를 들어 ELLT = 17번 이렇게
    apply_start_date = models.DateTimeField(null=True, blank=True) #신청 시작일
    apply_end_date = models.DateTimeField(null=True, blank=True) #신청 종료일
    priority_first = models.CharField(max_length=100, null=True, blank=True) # 학과 우선순위 기준 1 - 이거, 1대다로!!
    priority_second = models.CharField(max_length=100, null=True, blank=True) # 학과 우선순위 기준 2
    priority_third = models.CharField(max_length=100, null=True, blank=True) # 학과 우선순위 기준 3

    def __str__(self):
        return self.name # 학과 출력
    