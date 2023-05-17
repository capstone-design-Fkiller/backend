from django.db import models

from major.models import Major
from user.models import User
from locker.models import Building

class Apply(models.Model): #학생이 신청할 때 폼이다.
    id = models.BigAutoField(primary_key=True)
    major = models.ForeignKey(Major, related_name="apply", on_delete=models.PROTECT, db_column="major") # 학과의 아이디를 가져올 것. # 신청은 삭제가 될 수 있다
    user = models.ForeignKey(User, related_name="apply", on_delete=models.PROTECT, db_column="user") # 유저 아이디를 가져올 것.
    building_id = models.ForeignKey(Building, related_name="apply", on_delete=models.PROTECT, db_column="building_id")
    priority_1_answer = models.JSONField(null=True, blank=True) # 모두 null 인 경우 선착순 배정
    priority_2_answer = models.JSONField(null=True, blank=True)
    priority_3_answer = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "apply"
    
    def __str__(self):
        return self.id

class Sort(models.Model):
    priority = models.PositiveIntegerField(primary_key=True)
    apply = models.ForeignKey(Apply, related_name='sort', on_delete=models.CASCADE, db_column="apply")
    major = models.ForeignKey(Major, related_name='sort', on_delete=models.CASCADE, db_column="major", null=True, default=None)
    user = models.ForeignKey(User, related_name='sort', on_delete=models.CASCADE, db_column="user", null=True, default=None)
    building_id = models.ForeignKey(Building, related_name='sort', on_delete=models.CASCADE, db_column="building_id", null=True, default=None)
    priority_1_answer = models.JSONField(null=True, blank=True)
    priority_2_answer = models.JSONField(null=True, blank=True)
    priority_3_answer = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        db_table = "sort"
        ordering = ['priority']

    def __str__(self):
        return str(self.priority)

class Priority1(models.Model): #애는 하나의 유저당 하나씩 만들어져야 한다. 손명근한테 우리 학과 질문, 그에 대한 답변 , 123필요 없다. 한 개만 있으면 된다. first_criteria, first_answer
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Major, related_name="priority1", on_delete=models.PROTECT, db_column="priority1") #major의 자식으로 해서 first질문 받아 오도록
    answer = models.ForeignKey(Apply, related_name="priority1", on_delete=models.PROTECT, db_column="answer") #major의 자식으로 해서 first질문 받아 오도록

class Priority2(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Major, related_name="priority2", on_delete=models.PROTECT, db_column="priority2") #major의 자식으로 해서 first질문 받아 오도록
    answer = models.ForeignKey(Apply, related_name="priority2", on_delete=models.PROTECT, db_column="answer") #major의 자식으로 해서 first질문 받아 오도록

class Priority3(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Major, related_name="priority3", on_delete=models.PROTECT, db_column="priority3") #major의 자식으로 해서 first질문 받아 오도록
    answer = models.ForeignKey(Apply, related_name="priority3", on_delete=models.PROTECT, db_column="answer") #major의 자식으로 해서 first질문 받아 오도록
