import os
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse
import api
from api.config import DevelopmentConfig as dev_config
from api.config import ProductionConfig as prod_config
from api.utils.twitter_mongo import TwitterMongo
from api.utils import get_state_topic_google_news, get_us_news
from api.utils import reverse_states_map
from api.utils import get_daily_stats
from api.utils import get_daily_state_stats
from api.utils import read_county_data
from api.utils import read_country_data
from cachetools import cached, TTLCache


# Starts the FastAPI Router to be used by the FastAPI app.
router = APIRouter()
tm = TwitterMongo("covid", "twitter", verbose=False)


@router.get("/")
def root() -> str:
    """Root URL, for version checking.

    :param: none.
    :return: string. status string.
    """
    return f"COVID19 US Data API, Version {api.__version__}, Model. Status OK."


@router.get("/news")
def get_gnews() -> JSONResponse:
    """Fetch US news from Google News API and return it as a json string.

    TODO: Need to return the string of a pyhton dictionary

    :param: News object, with state and topic attribute string
    :return: JSONResponse of the topics fetched
    """
    try:
        data = get_us_news()
        json_data = {"success": True, "message": data}
    except Exception as ex:
        json_data = {"success": False, "message": f"Error occurred: {ex}"}
    return json_data


class News(BaseModel):
    state: str = "CA"
    topic: str = "Coronavirus"


@router.post("/news")
def post_gnews(news: News) -> JSONResponse:
    """Fetch specific state and topic news from Google News API and return it
    as a json string.

    TODO: Need to return the string of a pyhton dictionary

    :param: News object, with state and topic attribute string
    :return: JSONResponse of the topics fetched
    """
    try:
        state = reverse_states_map[news.state]
        data = get_state_topic_google_news(state, news.topic)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        json_data = {"success": False, "message": f"Error occured {ex}"}
    return json_data


@cached(cache=TTLCache(maxsize=1, ttl=3600))
@router.get("/county")
def get_county_data() -> JSONResponse:
    """
    Get all US county data and return it as a big fat json string.
    - Retrieves county locations, cached for 1 hour.
    
    :param: none.
    :return: JSONResponse
    """
    try:
        data = read_county_data()
        json_data = {"success": True, "message": data}
    except Exception as ex:
        json_data = {"success": False, "message": f"Error occured {ex}"}
    return json_data


@router.get("/stats")
def get_stats() -> JSONResponse:
    """Get overall tested, confirmed, and deaths stats from the database
    and return it as a json string. For the top bar.

    :param: none.
    :return: JSONResponse
    """
    try:
        data = get_daily_stats()
        json_data = {"success": True, "message": data}
    except Exception as ex:
        json_data = {"success": False, "message": f"Error occured {ex}"}
    return json_data


class Stats(BaseModel):
    state: str = "CA"


@router.post("/stats")
def post_stats(stats: Stats) -> JSONResponse:
    """Get overall tested, confirmed, and deaths stats from the database
    and return it as a json string. For the top bar.

    :param: none.
    :return: JSONResponse
    """
    try:
        data = get_daily_state_stats(stats.state)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        json_data = {"success": False, "message": f"Error occured {ex}"}
    return json_data


@router.get("/twitter")
def get_twitter() -> JSONResponse:
    """Fetch and return Twitter data from MongoDB connection.

    :param: none
    :return: str
    """
    try:
        doc = tm.get_tweet_by_state("US")
        username = doc["username"]
        full_name = doc["full_name"]
        tweets = doc["tweets"]
        # 2020-03-19 triage. lots of empty list at the end of tweets, filtering them out
        tweets = [*filter(None, tweets)]
        tweets = sorted(tweets, key=lambda i: i["created_at"], reverse=True)
        json_data = {
            "success": True,
            "message": {"username": username, "full_name": full_name, "tweets": tweets},
        }
    except Exception as ex:
        json_data = {"success": False, "message": f"Error occured {ex}"}
    return json_data


class TwitterUser(BaseModel):
    state: str


@router.post("/twitter")
def post_twitter(twyuser: TwitterUser) -> JSONResponse:
    """Fetch and return Twitter data from MongoDB connection.

    :param: none. Two letter state abbreviation.
    :return: str
    """
    try:
        doc = tm.get_tweet_by_state(twyuser.state)
        username = doc["username"]
        full_name = doc["full_name"]
        tweets = doc["tweets"]
        # 2020-03-19 triage. lots of empty list at the end of tweets, filtering them out
        tweets = [*filter(None, tweets)]
        tweets = sorted(tweets, key=lambda i: i["created_at"], reverse=True)
        json_data = {
            "success": True,
            "message": {"username": username, "full_name": full_name, "tweets": tweets},
        }
    except Exception as ex:
        json_data = {"success": False, "message": f"Error occured {ex}"}
    return json_data


class Country(BaseModel):
    alpha2Code: str


@cached(cache=TTLCache(maxsize=3, ttl=3600))
@router.post("/country")
def get_country(country: Country) -> JSONResponse:
    """Fetch country level data time series for Italy, US, and South Korea

    :param: none. Two letter state abbreviation.
    :return: json.  Schema:
    
    {"success": boolean
     "message": "[{"Italy": int, "US", int, "Korea, South", int},
                  {"Italy": int, "US", int, "Korea, South", int},
                 ]"
    }
    """
    cc = country.alpha2Code.upper()
    try:
        data = read_country_data(cc)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        json_data = {"success": False, "message": f"Error occured {ex}"}
    return json_data
