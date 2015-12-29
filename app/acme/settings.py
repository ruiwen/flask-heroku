
import os
import logging

from app.core.settings import DevConfig, ProdConfig, TestConfig

BLUEPRINTS = (
    {"name": "acme.widget.widgets", "url_prefix": "/widgets"},
)

INSTALLED_EXTENSIONS = ()

# Here we bootstrap the Config object, choosing one depending if we should be
# in PRODUCTION mode or not.
# This is followed by overriding set values with those set as envvars via
# read_env(), allowing for dynamic configuration in environments like Heroku
CONFIG = ProdConfig() if bool(os.getenv("PRODUCTION", False)) else DevConfig()

# Set up logging
if hasattr(CONFIG, 'LOGGING'):
    logging.config.dictConfig(CONFIG.LOGGING)
