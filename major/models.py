from django.db import models

# Create your models here.
class Priority(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    question = models.CharField(max_length=200)
    is_bool = models.BooleanField(default=True)
    is_ascending = models.BooleanField(default=False)

    class Meta:
        db_table = 'priority'

    def __str__(self):
        return self.name

class Major(models.Model): # 관리자들이 설정하는 학과 정보
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100) #학과명, 근데 이거는 학과명이 고유한 값으로 검색이 되어야 하는데, id로 하려면, 학과마다 번호를 붙여야할 수도 있겠다. 얘를 들어 ELLT = 17번 이렇게
    apply_start_date = models.DateTimeField(null=True, blank=True) #신청 시작일
    apply_end_date = models.DateTimeField(null=True, blank=True) #신청 종료일
    is_baserule_FCFS = models.BooleanField(default=True) # base rule이 선착순인지
    priority_1 = models.ForeignKey(Priority, related_name="major_priority_1", on_delete=models.PROTECT, db_column="priority_1", null=True, blank=True)
    priority_2 = models.ForeignKey(Priority, related_name="major_priority_2", on_delete=models.PROTECT, db_column="priority_2", null=True, blank=True)
    priority_3 = models.ForeignKey(Priority, related_name="major_priority_3", on_delete=models.PROTECT, db_column="priority_3", null=True, blank=True)


    class Meta:
        db_table = 'major'

    def __str__(self):
        return self.name # 학과 출력
