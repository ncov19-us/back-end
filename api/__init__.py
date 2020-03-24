"""Entry point for API """
# from api.config import PACKAGE_ROOT
from api.app import create_app
from api import endpoints
from api.config import DevelopmentConfig


APP = create_app(config_object=DevelopmentConfig)