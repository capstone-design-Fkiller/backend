from django.db import models

# Create your models here.


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.TextField() # front에서 암호화해서 보내줄 것으로 예상
    major = models.ForeignKey("major.Major", related_name="user", on_delete=models.PROTECT, db_column="major") #related_name = user로 수정
    penalty = models.BooleanField(default=False)
    penalty_start_date = models.DateTimeField(null=True, blank=True)
    penalty_end_date = models.DateTimeField(null=True, blank=True)
    id_card_img = models.TextField(default='')
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name


# # 선순위----------------------------------------------------------------------------------------------------------------------------

# class Major(models.Model): # 관리자들이 설정하는 학과 정보
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=100) #학과명, 근데 이거는 학과명이 고유한 값으로 검색이 되어야 하는데, id로 하려면, 학과마다 번호를 붙여야할 수도 있겠다. 얘를 들어 ELLT = 17번 이렇게
#     apply_start_date = models.DateTimeField() #신청 시작일
#     apply_end_date = models.DateTimeField() #신청 종료일
#     priority_first = models.CharField(max_length=100) # 학과 우선순위 기준 1 - 이거, 1대다로!!
#     priority_second = models.CharField(max_length=100, null=True, blank=True) # 학과 우선순위 기준 2
#     priority_third = models.CharField(max_length=100, null=True, blank=True) # 학과 우선순위 기준 3

#     def __str__(self):
#         return self.name # 학과 출력
    
# # 조인테이블이어야 되는 것이 아닌가? 얘는 
# class Priority1(models.Model): #애는 하나의 유저당 하나씩 만들어져야 한다. 손명근한테 우리 학과 질문, 그에 대한 답변 , 123필요 없다. 한 개만 있으면 된다. first_criteria, first_answer
#     id = models.BigAutoField(primary_key=True)
#     question = models.ForeignKey(Major) #Major의 pk, 즉 id를 가져온다.
#     answer = models.ForeignKey(Apply) #Major의 pk, 즉 id를 가져온다.
#     answer = models.CharField(max_length=100) #apply의 자식으로 답을 받아 오도록
#     # question = models.CharField(max_length=100, unique=True) #major의 자식으로 해서 first질문 받아 오도록

# class Priority2(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     question = models.CharField(max_length=100, unique=True, null=True, blank=True)
#     answer = models.CharField(max_length=100, null=True, blank=True) # 1대 다로 만들어서 가져올 수 있도록.

# class Priority3(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     question = models.CharField(max_length=100, unique=True, null=True, blank=True)
#     answer = models.CharField(max_length=100, null=True, blank=True)

# class Apply(models.Model): #학생이 신청할 때 폼이다.
#     id = models.BigAutoField(primary_key=True)
#     major = models.ForeignKey(Major) #Major의 pk, 즉 id를 가져온다.
#     user = models.ForeignKey(User, on_delete=models.CASCADE) # 이름
#     priority_1_answer = models.CharField(max_length=100)
#     priority_2_answer = models.CharField(max_length=100)
#     priority_3_answer = models.CharField(max_length=100)
#     # priority_1 = models.ForeignKey(Priority1, on_delete=models.CASCADE, related_name='apply_1', null=True, blank=True) #이거 이런식으로 쓰면 안된다. priority_1_answer = models.CharField(max_length=100) 이렇게 가야 한다. 얘는 입력을 받아야 한다. 외래키를 받는 게 아니라
#     # priority_2 = models.ForeignKey(Priority2, on_delete=models.CASCADE, related_name='apply_2', null=True, blank=True) #이거 이런식으로 쓰면 안된다. priority_1_answer = models.CharField(max_length=100) 이렇게 가야 한다. 얘는 입력을 받아야 한다. 외래키를 받는 게 아니라
#     # priority_3 = models.ForeignKey(Priority3, on_delete=models.CASCADE, related_name='apply_3', null=True, blank=True) #이거 이런식으로 쓰면 안된다. priority_1_answer = models.CharField(max_length=100) 이렇게 가야 한다. 얘는 입력을 받아야 한다. 외래키를 받는 게 아니라

# # major 도 있어야 할 거 같다.
# class Building(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=20)

# class Locker(models.Model): # 얘 만들려면 major db가 먼저 있어야 한다.
#     id = models.BigAutoField(primary_key=True)
#     building_id = models.IntegerField() # 빌딩은 int로 잘 되었고,
#     major = models.ForeignKey(Major) # 맞는지 모르겠다.
#     owned_id = models.ForeignKey(User, related_name='owned_lockers', null=True, blank=True) # 이건 맞고 
#     shared_id = models.ForeignKey(User, related_name='shared_lockers', null=True, blank=True) # 이것도 맞다.
#     is_share_registered = models.BooleanField(default=False) # 쉐어를 하겠다고 등록한 경우
#     start_date = models.DateTimeField(null=True, blank=True) # 대여 시작 날짜, 대여라는 이름을 붙여야겠다. 이름 헷갈린다.
#     end_date = models.DateTimeField(null=True, blank=True) # 대여 종료 날짜, 대여라는 이름을 붙여야겠다. 이름 헷갈린다.
#     share_start_date = models.DateTimeField(null=True, blank=True) # 쉐어 시작 날짜
#     share_end_date = models.DateTimeField(null=True, blank=True) # 쉐어 종료 날짜

# # 후순위----------------------------------------------------------------------------------------------------------------------------

# #관리자 나중에
# class Admin(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)
#     major = models.ForeignKey(Major)

#     def __str__(self):
#         return self.name


# # 게시글 나중에
# class Article(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     writer_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     major = models.ForeignKey(Major)

#     def __str__(self):
#         return self.title

# # 메시지 나중에
# class Message(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     writer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
