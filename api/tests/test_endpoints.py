import pytest
from starlette.testclient import TestClient
import api
from api import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here


def test_ping(test_app):
    response = test_app.get("/")
    assert response.status_code == 200


def test_get_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"success": True, 
                               "message": f"ncov19.us API, Version {api.__version__}, Status OK."}

                            
def test_get_news(test_app):
    pass


def test_post_news(test_app):
    pass


def test_get_twitter(test_app):
    pass


def test_post_twitter(test_app):
    pass


def test_get_county_data(test_app):
    pass


def test_post_county(test_app):
    pass


def test_post_state(test_app):
    pass


def test_get_country(test_app):
    pass


def test_get_stats(test_app):
    pass


def test_post_stats(test_app):
    pass
