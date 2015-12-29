
import os
import logging.config

from .config import Config


class DevConfig(Config):

    DEPLOYMENT = 'dev'
    #Server name needs to be the same as the hostname to avoid 404s.
    SERVER_NAME = "local.myserver.com:5000"
    SECRET_KEY = 'myversecretkey'
    DEBUG = True
    DB_DEFAULT = "mongodb://mydevvm/app"
    REDIS_URL = "redis://mydevvm:6379"
    REDIS_DB = 1

    AWS_ACCESS_KEY = "AKIAEXAMPLEKEYEXAMPL"
    AWS_SECRET_KEY = "secretsecretsecretsecretsecretsecretsect"
    MEDIA_BUCKET = 'my-media-bucket'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler'
            },
        },
        'loggers': {
            'app': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False
            }
        }
    }


class ProdConfig(DevConfig):

    DEPLOYMENT = 'prod'
    SERVER_NAME = "www.myserver.com"
    DEBUG = False
    DB_DEFAULT = "mongodb://myproddb/myapp"
    REDIS_URL = "redis://myprodredis:6379"
    REDIS_DB = 0


class TestConfig(DevConfig):
    pass


BLUEPRINTS = (
            )

INSTALLED_EXTENSIONS = (
                    )

# Here we bootstrap the Config object, choosing one depending if we should be
# in PRODUCTION mode or not.
CONFIG = ProdConfig() if bool(os.getenv("PRODUCTION", False)) else DevConfig(files=['settings_dev.cfg'])

# Set up logging
if hasattr(CONFIG, 'LOGGING'):
    logging.config.dictConfig(CONFIG.LOGGING)
