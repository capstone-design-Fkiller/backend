from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from major.models import Major


# 새로운 유저를 만드는 과정 되는구나. 일반 user는 django에 있다.
class UserManager(BaseUserManager):
    def create_user(self, id, password=None, major=None, **extra_fields):
        if not id:
            raise ValueError('The ID must be set')
        user = self.model(id=id, major=major, **extra_fields) #extra_fields가 다 알아서 넣어준다.
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    is_active = models.BooleanField(default=True) # 이 서비스를 사용가능한 유저 여부
    # is_staff = models.BooleanField(default=False) # 슈퍼유저 관련 - 얘는 없애야 돼
    name = models.CharField(max_length=20, default="")
    major = models.ForeignKey(Major, related_name="user", on_delete=models.PROTECT, db_column="major", null=True, blank=True) #related_name = user로 수정
    penalty = models.BooleanField(default=False)
    penalty_start_date = models.DateTimeField(null=True, blank=True)
    penalty_end_date = models.DateTimeField(null=True, blank=True)
    id_card_img = models.TextField(default='') # 길이 제한을 없애기 위해 text로 교체
    is_admin = models.BooleanField(default=False)
    # is_adminable = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True) # 없어도 될 거 같은데
    created_at = models.DateTimeField(auto_now_add=True)
    # password = models.TextField() # 얘는 장고가 알아서 생성해주는 걸로

    objects = UserManager()

    USERNAME_FIELD = 'id'
    # REQUIRED_FIELDS = []
    
    class Meta:
        """Meta definition for User."""

        #verbose_name = "User"
        #verbose_name_plural = "Users"
        db_table = "user"
    
    def __str__(self):
        return self.id
    

    # def create_user(self, id, password=None):
    #     if not id:
    #         raise ValueError('The ID must be set')

    #     user = self.model(id=id)
    #     user.set_password(password)
    #     major = self.validated_data.get('major') # 이녀석이 요물
    #     user.major = major
    #     id = self.validated_data.get('id')
    #     user.id = id
    #     user.name = self.validated_data.get('name')
    #     user.save(using=self._db)


    #     return user




# # 승희님 코드

# from accounts.validators import validate_username
# import re
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# def validate_username(username):
#     username_reg = r"^(?=.*[a-z])(?=.*\d)[a-z\d]{6,13}$"
#     username_regex = re.compile(username_reg)

#     if not username_regex.match(username):
#         raise ValidationError("영문+숫자 6자리 이상, 13자리 이하로 아이디 조합되어야합니다.")


# def validate_password(password):
#     password_reg = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,13}$"
#     password_regex = re.compile(password_reg)

#     if not password_regex.match(password):
#         raise ValidationError("영문, 숫자, 특수문자 조합해 6자 이상, 13자 이하 입력해주세요.")