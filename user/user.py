# from accounts.validators import validate_username
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# 새로운 유저를 만드는 과정 되는구나. 일반 user는 django에 있다.
class UserManager(BaseUserManager):
    def create_user(self, login_id, password=None):
        if not login_id:
            raise ValueError('The Login ID must be set')

        user = self.model(login_id=login_id)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    # REQUIRED_FIELDS = []
    
    class Meta:
        """Meta definition for User."""

        #verbose_name = "User"
        #verbose_name_plural = "Users"
        db_table = "users"
    
    def __str__(self):
        return self.id
    






# 승희님 코드
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