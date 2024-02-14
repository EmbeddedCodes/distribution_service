from frozen_dessert.settings.base import *
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'ICE-CREAM Distribution Service',
    'DESCRIPTION': 'ICE-CREAM Distribution Service API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

RQ_QUEUES = {
    "default": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        "DEFAULT_TIMEOUT": 360,
        'USE_REDIS_CACHE': 'default',
    },
}
