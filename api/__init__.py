"""Entry point for API """
from api.config import PACKAGE_ROOT
from api.app import create_app
from api.config import DevelopmentConfig, get_logger, Config

with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()

APP = create_app(config_object=DevelopmentConfig)
