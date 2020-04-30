import os
from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError, validator, Field
from pydantic.dataclasses import dataclass
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
from api.utils import read_county_stats
from api.utils import read_states
from cachetools import cached, TTLCache


# Starts the FastAPI Router to be used by the FastAPI app.
router = APIRouter()
tm = TwitterMongo("covid", "twitter", verbose=False)


###############################################################################
#
# Root Endpoint
#
################################################################################


class Message(BaseModel):
    message: str


class RootOutput(BaseModel):
    success: bool
    message: str


@router.get("/", response_model=RootOutput)
def root() -> JSONResponse:
    """Root URL, reporting version and status.
    """
    root_output = JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": f"ncov19.us API, Version {api.__version__}, Status OK.",
        },
    )
    return root_output


###############################################################################
#
# News Endpoints
#
################################################################################
class NewsInput(BaseModel):
    state: str = "CA"
    topic: str = "Coronavirus"


class News(BaseModel):
    title: str
    url: str
    published: str


class NewsOut(BaseModel):
    success: bool
    message: List[News]


@router.get("/news", response_model=NewsOut, responses={404: {"model": Message}})
def get_gnews() -> JSONResponse:
    """Fetch US news from Google News API and return the results in JSON
    """
    try:
        data = get_us_news()
        json_data = {"success": True, "message": data}
    except Exception as ex:
        return JSONResponse(
            status_code=404, content={"message": f"[Error] get /News API: {ex}"}
        )

    return json_data


@router.post("/news", response_model=NewsOut, responses={404: {"model": Message}})
def post_gnews(news: NewsInput) -> JSONResponse:
    """Fetch specific state and topic news from Google News API and return the
    results in JSON

    Input: NewsInput object schema, with state and topic attribute string
    Output: JSONResponse of the topics fetched
    """
    try:
        state = reverse_states_map[news.state]
        data = get_state_topic_google_news(state, news.topic)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        return JSONResponse(
            status_code=404, content={"message": f"[Error] post /News API: {ex}"}
        )

    return json_data


###############################################################################
#
# Twitter Feed Endpoints
#
################################################################################
class TwitterInput(BaseModel):
    state: str = "CA"


class Tweets(BaseModel):
    tweet_id: int
    full_text: str
    created_at: datetime


class UserTweets(BaseModel):
    username: str
    full_name: str
    tweets: List[Tweets] = None


class TwitterOutput(BaseModel):
    success: bool
    message: UserTweets


@router.get(
    "/twitter", response_model=TwitterOutput, responses={404: {"model": Message}}
)
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
        raise HTTPException(status_code=404, detail=f"[Error] get /twitter API: {ex}")

    return json_data


@router.post(
    "/twitter", response_model=TwitterOutput, responses={404: {"model": Message}}
)
def post_twitter(twyuser: TwitterInput) -> JSONResponse:
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
        raise HTTPException(status_code=404, detail=f"[Error] post /twitter API: {ex}")

    return json_data


###############################################################################
#
# County Endpoints
#
################################################################################
class CountyInput(BaseModel):
    state: str = "CA"
    county: str = "Orange"


class County(BaseModel):
    county_name: str = "New York"
    state_name: str = "New York"
    confirmed: int
    new: int
    death: int
    new_death: int
    fatality_rate: str = "1.2%"
    latitude: float
    longitude: float
    last_update: str = "2020-03-30 22:53 EDT"


class CountyOut(BaseModel):
    success: bool
    message: List[County]


@cached(cache=TTLCache(maxsize=1, ttl=3600))
@router.get("/county", response_model=CountyOut, responses={404: {"model": Message}})
def get_county_data() -> JSONResponse:
    """
    Get all US county data and return it as a big fat json string. Respond with
    404 if run into error.
    - Retrieves county locations, cached for 1 hour.
    
    :param: none.
    :return: JSONResponse
    """
    try:
        data = read_county_data()
        json_data = {"success": True, "message": data}
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"[Error] get '/county' API: {ex}")

    return json_data


@router.post("/county", response_model=CountyOut, responses={404: {"model": Message}})
def post_county(county: CountyInput) -> JSONResponse:
    """
    Get all US county data and return it as a big fat json string. Respond with
    404 if run into error.
    - Retrieves county locations, cached for 1 hour.
    
    :param: none.
    :return: JSONResponse
    """
    try:
        data = read_county_stats(county.state, county.county)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"[Error] get '/county' API: {ex}")

    return json_data

<<<<<<< HEAD
<<<<<<< HEAD
# @cached(cache=TTLCache(maxsize=1, ttl=3600))
@router.post("/county", response_model=CountyOut, responses={404: {"model": Message}})
def post_county_data() -> JSONResponse:
    """
    Get all US county data and return it as a big fat json string. Respond with
    404 if run into error.
    - Retrieves county locations, cached for 1 hour.
    
    :param: none.
    :return: JSONResponse
    """
    try:
        data = read_county_data()
        json_data = {"success": True, "message": data}
    except Exception as ex:
        raise HTTPException(status_code=404,
                            detail=f"[Error] get '/county' API: {ex}")

    return json_data
=======
>>>>>>> 04eca30... hursh: feat: added new post route for county
=======
>>>>>>> 794626a... han: ingest.py script, ingested all county data 3.2k+ rows and all country data aside from the princesses

###############################################################################
#
# State Endpoint
#
################################################################################
class StateInput(BaseModel):
    stateAbbr: str


class State(BaseModel):
    Date: str
    Confirmed: int
    Deaths: int


class StateOutput(BaseModel):
    success: bool
    message: List[State]


@cached(cache=TTLCache(maxsize=3, ttl=3600))
@router.post(
    "/state", response_model=StateOutput, responses={404: {"model": Message}}
)
def post_state(state: StateInput) -> JSONResponse:
    """Fetch state level data time series for a single state, ignoring the 
    unattributed and out of state cases.

    Input: two letter states code
    """

    try:
        data = read_states(state.stateAbbr)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"[Error] get /country API: {ex}")

    return json_data


###############################################################################
#
# Country Endpoint
#
################################################################################
class CountryInput(BaseModel):
    alpha2Code: str


class Country(BaseModel):
    Date: str
    Confirmed: int
    Deaths: int


class CountryOutput(BaseModel):
    success: bool
    message: List[Country]


@cached(cache=TTLCache(maxsize=3, ttl=3600))
@router.post(
    "/country", response_model=CountryOutput, responses={404: {"model": Message}}
)
def get_country(country: CountryInput) -> JSONResponse:
    """Fetch country level data time series for a single country

    Input: Two letter country alpha2Code
    """
    cc = country.alpha2Code.upper()
    try:
        data = read_country_data(cc)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"[Error] get /country API: {ex}")

    return json_data

###############################################################################
#
# Stats Endpoints
#
################################################################################
class StatsInput(BaseModel):
    state: str = "CA"


class Stats(BaseModel):
    tested: int
    todays_tested: int
    confirmed: int
    todays_confirmed: int
    deaths: int
    todays_deaths: int


class StatsOutput(BaseModel):
    success: bool
    message: Stats


@router.get("/stats", response_model=StatsOutput, responses={404: {"model": Message}})
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
        raise HTTPException(status_code=404, detail=f"[Error] get /stats API: {ex}")
    return json_data


@router.post("/stats", response_model=StatsOutput, responses={404: {"model": Message}})
def post_stats(stats: StatsInput) -> JSONResponse:
    """Get overall tested, confirmed, and deaths stats from the database
    and return it as a json string. For the top bar.

    :param: Stats
    :return: JSONResponse
    """
    try:
        data = get_daily_state_stats(stats.state)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        raise HTTPException(status_code=404, detail=f"[Error] post /stats API: {ex}")
    return json_data






# get:
# /daily
# US daily?
# /timeseries
# US time series?
# /info
# US info?

# post:
# /daily
#  {country, state, county} + {alpha2Code, stateabbrv, county name}



# /timeseries
#  {country, state, county} + {alpha2Code, stateabbrv, county name}
# # US time series?
# /info
# # US info?
#  {country, state, county} + {alpha2Code, stateabbrv, county name}