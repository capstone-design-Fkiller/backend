from django.db import models

from major.models import Major
from user.models import User
from locker.models import Building

# Create your models here.

# 조인테이블이어야 되는 것이 아닌가? 얘는 ????
class Priority1(models.Model): #애는 하나의 유저당 하나씩 만들어져야 한다. 손명근한테 우리 학과 질문, 그에 대한 답변 , 123필요 없다. 한 개만 있으면 된다. first_criteria, first_answer
    id = models.BigAutoField(primary_key=True)
    question = models.CharField(max_length=100, unique=True) #major의 자식으로 해서 first질문 받아 오도록
    answer = models.CharField(max_length=100, null=True, blank=True) #apply의 자식으로 답을 받아 오도록
    field_type = models.CharField(max_length=10, default='char')

# class Priority2(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     question = models.CharField(max_length=100, unique=True, null=True, blank=True)
#     answer = models.CharField(max_length=100, null=True, blank=True) # 1대 다로 만들어서 가져올 수 있도록.

# class Priority3(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     question = models.CharField(max_length=100, unique=True, null=True, blank=True)
#     answer = models.CharField(max_length=100, null=True, blank=True)

class Apply(models.Model): #학생이 신청할 때 폼이다.
    id = models.BigAutoField(primary_key=True)
    major = models.ForeignKey(Major, related_name="apply", on_delete=models.PROTECT, db_column="major") # 학과의 아이디를 가져올 것. # 신청은 삭제가 될 수 있다
    user = models.ForeignKey(User, related_name="apply", on_delete=models.PROTECT, db_column="user") # 유저 아이디를 가져올 것.
    building_id = models.ForeignKey(Building, related_name="apply", on_delete=models.PROTECT, db_column="building_id")
    priority_1 = models.ForeignKey(Priority1, on_delete=models.PROTECT, related_name='apply_1', null=True, blank=True)
    # priority_2 = models.ForeignKey(Priority2, on_delete=models.PROTECT, related_name='apply_2', null=True, blank=True)
    # priority_3 = models.ForeignKey(Priority3, on_delete=models.PROTECT, related_name='apply_3', null=True, blank=True)
    
    # priority_1_answer = models.CharField(max_length=100)
    # priority_2_answer = models.CharField(max_length=100)
    # priority_3_answer = models.CharField(max_length=100)

