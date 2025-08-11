import environ

env = environ.Env(
    DEBUG=(bool, True),
)

DEBUG = env("DEBUG")

if DEBUG:
    from .dev import *  # noqa
else:
    from .production import *  # noqa


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "HOST": "db",
        "PASSWORD": "postgres",
        "PORT": 5432,
    }
}
