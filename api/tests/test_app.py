import pytest
from starlette.testclient import TestClient
import api
from api import app


def test_app_headers(test_app = app):
    title = test_app.title
    description = test_app.description
    version = test_app.version
    assert title == "ncov19.us API"
    assert description == "API Support: ncov19us@gmail.com | URL: https://github.com/ncov19-us/back-end | [GNU GENERAL PUBLIC LICENSE](https://github.com/ncov19-us/back-end/blob/master/LICENSE)"
    assert version == f'{api.__version__}'
