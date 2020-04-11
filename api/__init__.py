"""Entry point for API """
from api.config import PACKAGE_ROOT
from api.app import create_app
from api.config import get_logger


with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()

app = create_app()
