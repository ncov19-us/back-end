# pylint: disable=redefined-outer-name
import json
import random
import pytest
from starlette.testclient import TestClient
from api import app


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


###############################################################################
#
#                   Test root endpoint
#
################################################################################
def test_get_root_redirect(test_app):
    """redirect response should be 307
    """
    response = test_app.get("/", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == \
        "https://documenter.getpostman.com/view/10962932/SzYevF7i"


def test_other_root(test_app):
    """Methods not allowed"""
    response = test_app.post("/")
    assert response.status_code == 405

    response = test_app.put("/")
    assert response.status_code == 405

    response = test_app.patch("/")
    assert response.status_code == 405

    response = test_app.delete("/")
    assert response.status_code == 405


###############################################################################
#
#                   Test News feed endpoints
#
################################################################################
def test_get_news(test_app):
    response = test_app.get("/news")
    assert response.status_code == 200


def test_post_news_validation(test_app):
    """Unprocessable entity"""
    response = test_app.post("/news")
    assert response.status_code == 422


def test_other_news(test_app):
    """Methods not allowed"""
    response = test_app.put("/news")
    assert response.status_code == 405

    response = test_app.patch("/news")
    assert response.status_code == 405

    response = test_app.delete("/news")
    assert response.status_code == 405


###############################################################################
#
#                   Test Twitter feed endpoints
#
################################################################################
def test_get_twitter(test_app):
    response = test_app.get("/twitter")
    data = response.json()['message']
    assert response.status_code == 200
    assert data['username'] == "CDCgov"
    assert data['full_name'] == "CDCgov"
    assert len(data['tweets']) > 0

    idx = random.randint(0, len(data['tweets']))
    assert 'tweet_id' in data['tweets'][idx]
    assert 'full_text' in data['tweets'][idx]
    assert 'created_at' in data['tweets'][idx]


def test_post_twitter(test_app):
    payload = {'state': 'TX'}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 200

    data = response.json()['message']
    assert data['username'] == "TexasDSHS"
    assert data['full_name'] == "Texas DSHS"
    assert len(data['tweets']) > 0

    idx = random.randint(0, len(data['tweets']))
    assert 'tweet_id' in data['tweets'][idx]
    assert 'full_text' in data['tweets'][idx]
    assert 'created_at' in data['tweets'][idx]


def test_post_twitter_validation(test_app):
    """Unprocessable entity"""
    response = test_app.post("/twitter")
    assert response.status_code == 422

    # TODO: /twitter post has no input validation, so still return 200
    payload = {'testing': 'validation'}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 200


def test_post_twitter_not_found(test_app):
    """data not found"""

    # /twitter post endpoint has state input field, this should return 404
    payload = {'state': 'validation'}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 404

    # /twitter post endpoint takes state abbreviations capitalized, expect 404
    payload = {'state': 'California'}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 404

    # /twitter post endpoint takes state abbreviations capitalized, expect 404
    payload = {'state': 'maine'}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 404

    # /twitter post endpoint takes state abbreviations capitalized, expect 404
    payload = {'state': 'mi'}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 404


def test_other_twitter(test_app):
    """Methods not allowed"""
    response = test_app.put("/twitter")
    assert response.status_code == 405

    response = test_app.patch("/twitter")
    assert response.status_code == 405

    response = test_app.delete("/twitter")
    assert response.status_code == 405


###############################################################################
#
#                   Test county data endpoints
#
################################################################################
def test_get_county_data(test_app):
    response = test_app.get("/county")
    assert response.status_code == 200


def test_post_county_validation(test_app):
    """Unprocessable entity"""
    response = test_app.post("/county")
    assert response.status_code == 422

    # TODO: /county post has no input validation, so still return 200
    payload = {'testing': 'validation'}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 200

    # TODO: /county post has no input validation, so still return 200
    payload = {'testing': 'validation', 'this': 'shouldnt work'}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 200


def test_post_county_not_found(test_app):
    """data not found"""

    payload = {'state': 'validation', 'county': 'shouldnt work'}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404

    payload = {'state': 'CA', 'county': 'shouldnt work'}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404

    payload = {'state': 'shouldnt work', 'county': 'orange'}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404

    payload = {'state': 'CA', 'county': 'orange'}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404

    payload = {'state': 'ca', 'county': 'Orange'}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404


def test_other_county(test_app):
    """Methods not allowed"""
    response = test_app.put("/county")
    assert response.status_code == 405

    response = test_app.patch("/county")
    assert response.status_code == 405

    response = test_app.delete("/county")
    assert response.status_code == 405


###############################################################################
#
#                   Test state endpoints
#
################################################################################
def test_post_state_validation(test_app):
    """Unprocessable entity"""
    response = test_app.post("/state")
    assert response.status_code == 422


def test_other_state(test_app):
    """Methods not allowed"""
    response = test_app.get("/state")
    assert response.status_code == 405

    response = test_app.put("/state")
    assert response.status_code == 405

    response = test_app.patch("/state")
    assert response.status_code == 405

    response = test_app.delete("/state")
    assert response.status_code == 405


###############################################################################
#
#                   Test country endpoints
#
################################################################################
def test_post_country_validation(test_app):
    """Unprocessable entity"""
    response = test_app.post("/country")
    assert response.status_code == 422


def test_other_country(test_app):
    """Methods not allowed"""
    response = test_app.get("/country")
    assert response.status_code == 405

    response = test_app.put("/country")
    assert response.status_code == 405

    response = test_app.patch("/country")
    assert response.status_code == 405

    response = test_app.delete("/country")
    assert response.status_code == 405


###############################################################################
#
#                   Test stats endpoints
#
################################################################################
def test_get_stats(test_app):
    response = test_app.get("/stats")
    assert response.status_code == 200


def test_post_stats_validation(test_app):
    """Unprocessable entity"""
    response = test_app.post("/stats")
    assert response.status_code == 422


def test_other_stats(test_app):
    """Methods not allowed"""
    response = test_app.put("/stats")
    assert response.status_code == 405

    response = test_app.patch("/stats")
    assert response.status_code == 405

    response = test_app.delete("/stats")
    assert response.status_code == 405
