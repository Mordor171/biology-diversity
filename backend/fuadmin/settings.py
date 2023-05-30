"""
Django settings for fuadmin project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path
from conf.env import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xxxxxx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = locals().get('DEBUG', True)
ALLOWED_HOSTS = locals().get('ALLOWED_HOSTS', ['*'])
DEMO = locals().get('DEMO', False)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'system',
    'biology',
    # 添加验证码功能
    'captcha'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware.ApiLoggingMiddleware',

]

ROOT_URLCONF = 'fuadmin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fuadmin.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]

STATICFILES_FINDERS = (

"django.contrib.staticfiles.finders.FileSystemFinder",

"django.contrib.staticfiles.finders.AppDirectoriesFinder"

)
# 访问上传文件的url地址前缀
# MEDIA_URL = "/media/"
# 项目中存储上传文件的根目录
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'system.Users'
USERNAME_FIELD = 'username'
ALL_MODELS_OBJECTS = []  # 所有app models 对象

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
# 数据库配置
if DATABASE_TYPE == "MYSQL":
    # Mysql数据库
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": DATABASE_HOST,
            "PORT": DATABASE_PORT,
            "USER": DATABASE_USER,
            "PASSWORD": DATABASE_PASSWORD,
            "NAME": DATABASE_NAME,
        }
    }
elif DATABASE_TYPE == "SQLSERVER":
    # SqlServer数据库
    DATABASES = {
        "default": {
            "ENGINE": "mssql",
            "HOST": DATABASE_HOST,
            "PORT": DATABASE_PORT,
            "USER": DATABASE_USER,
            "PASSWORD": DATABASE_PASSWORD,
            "NAME": DATABASE_NAME,
            # 全局开启事务，绑定的是http请求响应整个过程
            'ATOMIC_REQUESTS': True,
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
            },
        }
    }
else:
    # sqlite3 数据库
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'OPTIONS': {
                'timeout': 20,
            },
        }
    }

# 缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'{REDIS_URL}/1',
        "TIMEOUT": None,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# celery 配置
CELERY_BROKER_URL = f'{REDIS_URL}/2'
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_ENABLE_UTC = False
CELERY_WORKER_CONCURRENCY = 2  # 并发数
CELERY_MAX_TASKS_PER_CHILD = 5  # 没个worker最多执行5个任务便自我销毁释放内存
CELERY_TIMEZONE = TIME_ZONE  # celery 时区问题
CELERY_RESULT_BACKEND = 'django-db'  # celery结果存储到数据库中
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'  # Backend数据库

# token 有效时间 时 分 秒
TOKEN_LIFETIME = 12 * 60 * 60
# TOKEN_LIFETIME = 50

# 接口白名单，不需要授权直接访问
WHITE_LIST = ['/api/system/userinfo', '/api/system/getCode', '/api/system/permCode', '/api/system/menu/route/tree', '/api/system/upload']

# 接口日志记录
API_LOG_ENABLE = True
API_LOG_METHODS = ['POST', 'GET', 'DELETE', 'PUT']
API_MODEL_MAP = {}


# 初始化需要执行的列表，用来初始化后执行
INITIALIZE_RESET_LIST = []

# 验证码配置
# CAPTCHA_OUTPUT_FORMAT是设设置三者的显示顺序
CAPTCHA_OUTPUT_FORMAT = '%(text_field)s %(hidden_field)s %(image)s'
# 设置图片噪点
CAPTCHA_NOISE_FUNCTIONS = (
    # 设置样式
    'captcha.helpers.noise_null',
    # 设置干扰线
    'captcha.helpers.noise_arcs',
    # 设置干扰点
    'captcha.helpers.noise_dots',
)

# 图片大小
CAPTCHA_IMAGE_SIZE = (100, 25)
# 设置图片背景颜色
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
# 图片中的文字为随机英文字母
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
# 图片中的文字为英文单词
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'
# 图片中的文字为数字表达式
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
# 设置字符个数
CAPTCHA_LENGTH = 4
# 设置超时时间(minutes)
CAPTCHA_TIMEOUT = 1


#oss配置
#your keyid
ACCESS_KEY_ID = "xxxxxx"
#your keyidsecret
ACCESS_KEY_SECRET = "xxxxxx"
#your endpoint
EndPoint = "xxxxxx"
#your projectname
ProjectName = "xxxxxx"
#your bucketUrl
Base_File_URL = "xxxxxx"