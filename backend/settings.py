"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import my_settings
import pymysql
from datetime import datetime, timedelta
from corsheaders.defaults import default_headers


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = my_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "major",
    "apply",
    "locker",
    "alert",
    "notice",
    "assign",
    "rest_framework",
    "drf_yasg",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    'corsheaders',
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "django_seed",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS_ORIGIN_ALLOW_ALL = True # 모든 URL 허용
CORS_ALLOW_CREDENTIALS = True # 쿠키 설정


CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:3000',
    'https://127.0.0.1:3000',
    'http://127.0.0.1:5173',
    'https://127.0.0.1:5173',
    'http://127.0.0.1:5174',
    'http://127.0.0.1:5713',
    'https://127.0.0.1:5713',
    'https://127.0.0.1:5174',
    'http://127.0.0.1:5714',
    'https://127.0.0.1:5714',
    'http://127.0.0.1:8001',
    'https://127.0.0.1:8001',
    'http://localhost:3000',
    'https://localhost:3000',
    'http://localhost:5173',
    'http://localhost:5173',
    'https://localhost:5173',
    'http://localhost:5174',
    'http://localhost:5713',
    'https://localhost:5713',
    'https://localhost:5174',
    'http://localhost:5714',
    'https://localhost:5714',
    'http://localhost:8001',
    'https://localhost:8001',
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'access_token', # 허용할 헤더 필드 추가
    'refresh_token',
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()

DATABASES = my_settings.DATABASES

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'id'
ACCOUNT_USERNAME_REQUIRED = False

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'user.serializers.MyUserRegistrationSerializer'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
    # 'rest_framework.permissions.IsAuthenticated', # 인증된 사용자만 접근
    # 'rest_framework.permissions.IsAdminUser', # 관리자만 접근
    'rest_framework.permissions.AllowAny', # 누구나 접근
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

}


AUTH_USER_MODEL = 'user.User'


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
