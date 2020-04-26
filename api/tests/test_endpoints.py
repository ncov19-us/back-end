# pylint: disable=redefined-outer-name

import time
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
    assert response.headers["location"] == "/redoc"


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
    data = response.json()["message"]
    assert response.status_code == 200
    assert data["username"] == "CDCgov"
    assert data["full_name"] == "CDCgov"
    assert len(data["tweets"]) > 0

    idx = random.randint(0, len(data["tweets"]))
    assert "tweet_id" in data["tweets"][idx]
    assert "full_text" in data["tweets"][idx]
    assert "created_at" in data["tweets"][idx]


def test_post_twitter(test_app):
    payload = {"state": "TX"}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 200

    data = response.json()["message"]
    assert data["username"] == "TexasDSHS"
    assert data["full_name"] == "Texas DSHS"
    assert len(data["tweets"]) > 0

    idx = random.randint(0, len(data["tweets"]))
    assert "tweet_id" in data["tweets"][idx]
    assert "full_text" in data["tweets"][idx]
    assert "created_at" in data["tweets"][idx]


def test_post_twitter_validation(test_app):
    """Unprocessable entity"""
    response = test_app.post("/twitter")
    assert response.status_code == 422

    # TODO: /twitter post has no input validation, so still return 200
    payload = {"testing": "validation"}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 200


def test_post_twitter_not_found(test_app):
    """data not found"""

    # /twitter post endpoint has state input field, this should return 404
    payload = {"state": "validation"}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 404

    # /twitter post endpoint takes state abbreviations capitalized, expect 404
    payload = {"state": "California"}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 404

    # /twitter post endpoint takes state abbreviations capitalized, expect 404
    payload = {"state": "maine"}
    response = test_app.post("/twitter", data=json.dumps(payload))
    assert response.status_code == 404

    # /twitter post endpoint takes state abbreviations capitalized, expect 404
    payload = {"state": "mi"}
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
    payload = {"testing": "validation"}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 200

    # TODO: /county post has no input validation, so still return 200
    payload = {"testing": "validation", "this": "shouldnt work"}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 200


def test_post_county_not_found(test_app):
    """data not found"""

    payload = {"state": "validation", "county": "shouldnt work"}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404

    payload = {"state": "CA", "county": "shouldnt work"}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404

    payload = {"state": "shouldnt work", "county": "orange"}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404

    payload = {"state": "CA", "county": "orange"}
    response = test_app.post("/county", data=json.dumps(payload))
    assert response.status_code == 404

    payload = {"state": "ca", "county": "Orange"}
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


###############################################################################
#
#                   Test county data endpoints
#
################################################################################
def test_post_ny_zip(test_app):
    """Test problematic zip codes:
    10004 -> Manhattan (New York County), NY
    10302 -> Staten Island (Richmond County), NY
    10458 -> Bronx, NY
    11203 -> Brooklyn (Kings County), NY
    11361 -> Queens (Queens County), NY
    """
    payload = {"zip_code": "10004"}
    response = test_app.post("/zip", data=json.dumps(payload))
    time.sleep(2)
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "New York"
    assert data["county_name"] == "New York"

    payload = {"zip_code": "10312"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "New York"
    # TODO: add Richmond county
    # assert data['county_name'] == "Richmond"
    assert data["county_name"] == "New York"

    payload = {"zip_code": "10458"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "New York"
    # TODO: add Bronx county
    # assert data['county_name'] == "Bronx"
    assert data["county_name"] == "New York"


def test_post_nyc_borough_zip(test_app):
    """Test problematic zip codes:
    10004 -> Manhattan (New York County), NY
    10302 -> Staten Island (Richmond County), NY
    10458 -> Bronx, NY
    11203 -> Brooklyn (Kings County), NY
    11361 -> Queens (Queens County), NY
    """
    payload = {"zip_code": "10004"}
    response = test_app.post("/zip", data=json.dumps(payload))
    time.sleep(2)
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "New York"
    assert data["county_name"] == "New York"

    payload = {"zip_code": "10312"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "New York"
    # TODO: add Richmond county
    # assert data['county_name'] == "Richmond"
    assert data["county_name"] == "New York"

    payload = {"zip_code": "10458"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "New York"
    # TODO: add Bronx county
    # assert data['county_name'] == "Bronx"
    assert data["county_name"] == "New York"

    payload = {"zip_code": "11203"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "New York"
    # TODO: add Brooklyn/Kings county
    # assert data['county_name'] == "Brooklyn"
    assert data["county_name"] == "New York"

    payload = {"zip_code": "11361"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "New York"
    # TODO: add Queens/Queens county
    # assert data['county_name'] == "Queens"
    assert data["county_name"] == "New York"


def test_post_zip(test_app):
    """Test problematic zip codes:
    04098 -> Cumberland, Maine
    63163 -> Saint Louis, MO
    70030 -> St. Charles, LA
    70341 -> Assumption Parish, LA
    """
    payload = {"zip_code": "04098"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Maine"
    assert data["county_name"] == "Cumberland"

    payload = {"zip_code": "63163"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Missouri"
    assert data["county_name"] == "St. Louis"

    payload = {"zip_code": "70030"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Louisiana"
    assert data["county_name"] == "St. Charles"

    payload = {"zip_code": "70341"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Louisiana"
    assert data["county_name"] == "Assumption"

    payload = {"zip_code": "99352"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Washington"
    assert data["county_name"] == "Benton and Franklin"


def test_post_zip_data_source_adjustments(test_app):
    """Test problematic zip codes:
    02552 -> Dukes County, MA (Dukes and Nantucket in data source)
    02584 -> Nantucket County, MA (Dukes and Nantucket in data source)
    48212 -> Detroit, MI (Wayne County)
    77003 -> Houston, TX (Harris County)
    75847 -> Houston County, TX (which is not Houston city)
    99326 -> Franklin County, WA (Benton and Franklin in data source)
    99352 -> Benton County, WA (Benton and Franklin in data source)
    """
    payload = {"zip_code": "02552"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Massachusetts"
    assert data["county_name"] == "Dukes and Nantucket"

    payload = {"zip_code": "02584"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Massachusetts"
    assert data["county_name"] == "Dukes and Nantucket"

    payload = {"zip_code": "48212"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Michigan"
    assert data["county_name"] == "Wayne"

    payload = {"zip_code": "77003"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Texas"
    assert data["county_name"] == "Harris"

    payload = {"zip_code": "75847"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Texas"
    assert data["county_name"] == "Houston"

    payload = {"zip_code": "99326"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Washington"
    assert data["county_name"] == "Benton and Franklin"

    payload = {"zip_code": "99352"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200
    data = response.json()["message"]
    assert data["state_name"] == "Washington"
    assert data["county_name"] == "Benton and Franklin"


def test_post_zip_us_districs_and_territories(test_app):
    """
    20037 -> Washington DC
    00601 -> Puerto Rico, Puerto Rico
    96910 -> Guam, Guam
    96950 -> Northern Mariana Islands, Northern Mariana Islands
    00801 -> St. Thomas, US Virgin Islands
    00830 -> St. John, US Virgin Islands
    00820 -> St. Croix, US Virgin Islands (City - Christiansted)
    00840 -> St. Croix, US Virgin Islands (City - Frederiksted)
    00850 -> St. Croix, US Virgin Islands (City - Kingshill)
    """

    expected_data = [
        {
            "zip_code": "20037",
            "state_name": "District of Columbia",
            "county_name": "District of Columbia",
        },
        {
            "zip_code": "00601",
            "state_name": "Puerto Rico",
            "county_name": "Puerto Rico",
        },
        {"zip_code": "96910", "state_name": "Guam", "county_name": "Guam"},
        {
            "zip_code": "96950",
            "state_name": "Northern Mariana Islands",
            "county_name": "Northern Mariana Islands",
        },
        {
            "zip_code": "00801",
            "state_name": "St. Thomas",
            "county_name": "US Virgin Islands",
        },
        {
            "zip_code": "00830",
            "state_name": "St. John",
            "county_name": "US Virgin Islands",
        },
        {
            "zip_code": "00820",
            "state_name": "St. Croix",
            "county_name": "US Virgin Islands",
        },
        {
            "zip_code": "00840",
            "state_name": "St. Croix",
            "county_name": "US Virgin Islands",
        },
        {
            "zip_code": "00850",
            "state_name": "St. Croix",
            "county_name": "US Virgin Islands",
        },
    ]
    for data in expected_data:
        payload = {"zip_code": data["zip_code"]}
        response = test_app.post("/zip", data=json.dumps(payload))
        assert response.status_code == 200
        data = response.json()["message"]
        assert data["state_name"] == data["state_name"]
        assert data["county_name"] == data["county_name"]


def test_post_zip_validation(test_app):
    """Unprocessable entity"""
    response = test_app.post("/zip")
    assert response.status_code == 422

    # TODO: /zip post has no input validation, so still return 200
    payload = {"testing": "validation"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200

    # TODO: /zip post has no input validation, so still return 200
    payload = {"testing": "validation", "this": "shouldnt work"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 200


def test_post_zip_not_found(test_app):
    """invalid zip codes"""

    payload = {"zip_code": "33333"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 422

    payload = {"zip_code": "90000"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 422

    payload = {"zip_code": "20000"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 422

    payload = {"zip_code": "72200"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 422

    payload = {"zip_code": "75874"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 422

    payload = {"zip_code": "57400"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 422

    payload = {"zip_code": "123456"}
    response = test_app.post("/zip", data=json.dumps(payload))
    assert response.status_code == 422


def test_other_zip(test_app):
    """Methods not allowed"""
    response = test_app.put("/zip")
    assert response.status_code == 405

    response = test_app.patch("/zip")
    assert response.status_code == 405

    response = test_app.delete("/zip")
    assert response.status_code == 405
