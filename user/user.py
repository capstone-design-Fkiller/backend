# from accounts.validators import validate_username
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# 승희님 코드
def validate_username(username):
    username_reg = r"^(?=.*[a-z])(?=.*\d)[a-z\d]{6,13}$"
    username_regex = re.compile(username_reg)

    if not username_regex.match(username):
        raise ValidationError("영문+숫자 6자리 이상, 13자리 이하로 아이디 조합되어야합니다.")


def validate_password(password):
    password_reg = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,13}$"
    password_regex = re.compile(password_reg)

    if not password_regex.match(password):
        raise ValidationError("영문, 숫자, 특수문자 조합해 6자 이상, 13자 이하 입력해주세요.")


# 새로운 유저를 만드는 과정 되는구나. 일반 user는 django에 있다.
class CustomUserManager(BaseUserManager):
    def create_user(self, login_id, password=None):
        if not login_id:
            raise ValueError('The Login ID must be set')

        user = self.model(login_id=login_id)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id, password):
        user = self.create_user(login_id=login_id, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    login_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login_id
    


# 관리자 사용자 모델 - email 지우기
class MyAdminUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class MyAdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = MyAdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email







### 여기는 email 있는 버전

# class CustomUserManager(BaseUserManager):
#     def create_user(self, login_id, email, password=None, **extra_fields):
#         if not login_id:
#             raise ValueError('The Login ID field must be set')
#         email = self.normalize_email(email)
#         user = self.model(login_id=login_id, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, login_id, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(login_id, email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     login_id = models.CharField(max_length=30, unique=True)
#     email = models.EmailField(max_length=254, unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'login_id'
#     EMAIL_FIELD = 'email'

#     def __str__(self):
#         return self.login_id




class UserManager(BaseUserManager):
    def create_user(self, email, nickname, username, password=None):
        if not email:
            raise ValueError("must have user email")
        if not nickname:
            raise ValueError("must have user nickname")
        if not username:
            raise ValueError("must have username")
        user = self.model(
            email=self.normalize_email(email), nickname=nickname, username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, nickname, username, password=None): # 슈퍼 유저는 필요 없으니까 삭제
    #     user = self.create_user(
    #         email, password=password, nickname=nickname, username=username
    #     )
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user


def profile_img_upload_path(instance, filename):
    return "profile_img/user_{}/{}".format(instance.username, filename)


class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User."""

    USERNAME_FIELD = "login_id"
    # REQUIRED_FIELDS = ["email", "nickname", "password"]

    # GENDER_CHOICES = (
    #     ("M", "Male"),
    #     ("F", "Female"),
    #     ("NB", "Non_Binary"),
    # )

    email = models.EmailField(
        verbose_name=_("email"),
        max_length=200,
        unique=True,
    )
    username = models.CharField(
        verbose_name=_("username"),
        max_length=50,
        unique=True,
        validators=[validate_username],
    )

    nickname = models.CharField(
        max_length=100,
        unique=True,
        error_messages={"unique": "A user with that nickname already exists."},
        null=False,
    )
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    profile_img = models.ImageField(
        null=True, blank=True, verbose_name="프로필 이미지", upload_to=profile_img_upload_path
    )
    introduce = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="사용자 소개",
        default="사용자 소개가 없습니다.",
    )
    agree_prefragrance = models.BooleanField(default=False)
    agree_personal_required = models.BooleanField(default=False)

    is_active = models.BooleanField(
        verbose_name=_("Is active"),
        default=True,
    )

    objects = UserManager()

    class Meta:
        """Meta definition for User."""

        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser