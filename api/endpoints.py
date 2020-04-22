import gc
from typing import List
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse, RedirectResponse
from cachetools import cached, TTLCache
import zipcodes

from api.config import app_config
from api.config import get_logger
from api.utils.twitter_mongo import TwitterMongo
from api.utils import get_state_topic_google_news, get_us_news
from api.utils import reverse_states_map
from api.utils import get_daily_stats
from api.utils import get_daily_state_stats
from api.utils import read_county_data
from api.utils import read_country_data
from api.utils import read_county_stats
from api.utils import read_states
# from api.utils import read_county_stats_zip_ny
from api.config import DataReadingError

# Starts the FastAPI Router to be used by the FastAPI app.
router = APIRouter()
_logger = get_logger(logger_name=__name__)
tm = TwitterMongo(app_config.DB_NAME,
                  app_config.COLLECTION_TWITTER,
                  verbose=False)


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


@router.get("/")#, response_model=RootOutput)
async def root() -> JSONResponse:
    """Root URL, redirect to ReDoc API doc
    """
    _logger.info("Endpoint: / --- GET - redirect")
    url = "/redoc"
    response = RedirectResponse(url=url)

    return response


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


@router.get("/news",
            response_model=NewsOut,
            responses={404: {"model": Message}})
async def get_gnews() -> JSONResponse:
    """Fetch US news from Google News API and return the results in JSON
    """
    try:
        data = get_us_news()
        json_data = {"success": True, "message": data}
        del data
        gc.collect()
    except DataReadingError as ex:
        _logger.warning(f"Endpoint: /news --- GET --- {ex}")
        return JSONResponse(
            status_code=404, content={"message": f"[Error] get /News API: {ex}"}
        )

    return json_data


@router.post("/news",
             response_model=NewsOut,
             responses={404: {"model": Message}})
async def post_gnews(news: NewsInput) -> JSONResponse:
    """Fetch specific state and topic news from Google News API and return the
    results in JSON
    """
    try:
        state = reverse_states_map[news.state]
        data = get_state_topic_google_news(state, news.topic)
        json_data = {"success": True, "message": data}
        del data
        gc.collect()
    except DataReadingError as ex:
        _logger.warning(f"Endpoint: /news --- POST --- {ex}")
        return JSONResponse(
            status_code=404,
            content={"message": f"[Error] post /News API: {ex}"}
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


@router.get("/twitter",
            response_model=TwitterOutput,
            responses={404: {"model": Message}})
async def get_twitter() -> JSONResponse:
    """Fetch and return Twitter data from MongoDB connection."""
    try:
        doc = tm.get_tweet_by_state("US")
        username = doc["username"]
        full_name = doc["full_name"]
        tweets = doc["tweets"]

        # 2020-03-19 triage. filtering out empty list at the end of tweets
        tweets = [*filter(None, tweets)]
        tweets = sorted(tweets, key=lambda i: i["created_at"], reverse=True)

        json_data = {
            "success": True,
            "message": {"username": username,
                        "full_name": full_name,
                        "tweets": tweets},
        }
        del tweets
        gc.collect()
    except Exception as ex:
        _logger.warning(f"Endpoint: /twitter --- GET --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] get /twitter API: {ex}")

    return json_data


@router.post("/twitter",
             response_model=TwitterOutput,
             responses={404: {"model": Message}})
async def post_twitter(twyuser: TwitterInput) -> JSONResponse:
    """Fetch and return Twitter data from MongoDB connection."""
    try:
        doc = tm.get_tweet_by_state(twyuser.state)
        username = doc["username"]
        full_name = doc["full_name"]
        tweets = doc["tweets"]
        # 2020-03-19 triage. filtering out empty list at the end of tweets
        tweets = [*filter(None, tweets)]
        tweets = sorted(tweets, key=lambda i: i["created_at"], reverse=True)
        json_data = {
            "success": True,
            "message": {"username": username,
                        "full_name": full_name,
                        "tweets": tweets},
        }

        del tweets
        gc.collect()
    except Exception as ex:
        _logger.warning(f"Endpoint: /twitter --- POST --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] post /twitter API: {ex}")

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
@router.get("/county",
            response_model=CountyOut,
            responses={404: {"model": Message}})
async def get_county_data() -> JSONResponse:
    """Get all US county data and return it as a big fat json string. Respond
    with 404 if run into error.
    - Cached for 1 hour.
    """
    try:
        data = read_county_data()
        json_data = {"success": True, "message": data}
        del data
        gc.collect()
    except Exception as ex:
        _logger.warning(f"Endpoint: /county --- GET --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] get '/county' API: {ex}")

    return json_data


@router.post("/county",
             response_model=CountyOut,
             responses={404: {"model": Message}})
def post_county(county: CountyInput) -> JSONResponse:
    """Get all US county data and return it as a big fat json string. Respond
    with 404 if run into error.
    """
    try:
        data = read_county_stats(county.state, county.county)
        json_data = {"success": True, "message": data}
        del data
        gc.collect()
    except Exception as ex:
        _logger.warning(f"Endpoint: /county --- POST --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] get '/county' API: {ex}")

    return json_data

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
@router.post("/state",
             response_model=StateOutput,
             responses={404: {"model": Message}})
async def post_state(state: StateInput) -> JSONResponse:
    """Fetch state level data time series for a single state, ignoring the
    unattributed and out of state cases.
    - Cached for 1 hour
    """

    try:
        data = read_states(state.stateAbbr)
        json_data = {"success": True, "message": data}
        del data
        gc.collect()
    except Exception as ex:
        _logger.warning(f"Endpoint: /state --- POST --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] get /country API: {ex}")

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
@router.post("/country",
             response_model=CountryOutput,
             responses={404: {"model": Message}})
async def get_country(country: CountryInput) -> JSONResponse:
    """Fetch country level data time series for a single country.
    - Cached for 1 hour
    """
    cc = country.alpha2Code.upper()
    try:
        data = read_country_data(cc)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        _logger.warning(f"Endpoint: /country --- GET --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] get /country API: {ex}")

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


@router.get("/stats",
            response_model=StatsOutput,
            responses={404: {"model": Message}})
async def get_stats() -> JSONResponse:
    """Get overall tested, confirmed, and deaths stats from the database
    and return it as a JSON string.
    """
    try:
        data = get_daily_stats()
        json_data = {"success": True, "message": data}
    except Exception as ex:
        _logger.warning(f"Endpoint: /stats --- GET --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] get /stats API: {ex}")
    return json_data


@router.post("/stats",
             response_model=StatsOutput,
             responses={404: {"model": Message}})
async def post_stats(stats: StatsInput) -> JSONResponse:
    """Get overall tested, confirmed, and deaths stats from the database
    and return it as a JSON string.
    """
    try:
        data = get_daily_state_stats(stats.state)
        json_data = {"success": True, "message": data}
    except Exception as ex:
        _logger.warning(f"Endpoint: /stats --- POST --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] post /stats API: {ex}")
    return json_data

###############################################################################
#
# ZIP Endpoint
#
################################################################################
class ZIPInput(BaseModel):
    zip_code: str = "70030"

class ZIPStats(BaseModel):
    county_name: str = "St. Charles"
    state_name: str = "Louisiana"
    confirmed: int
    new: int
    death: int
    new_death: int
    fatality_rate: str = "5.5%"
    latitude: float
    longitude: float
    last_update: str = "2020-04-17 19:50 EDT"

class ZIPOutput(BaseModel):
    success: bool
    message: ZIPStats


@router.post("/zip",
             response_model=ZIPOutput,
             responses={404: {"model": Message}})
def post_zip(zip_code: ZIPInput) -> JSONResponse:
    """Returns county stats for the zip code input.
    """

    try:
        zip_info = zipcodes.matching(zip_code.zip_code)[0]
    except Exception as ex:
        message = (f"ZIP code {zip_code.zip_code}"
                    " not found in US Zipcode database.")
        _logger.warning(f"Endpoint: /zip --- POST --- {ex} {message}")
        raise HTTPException(status_code=422,
                            detail=f"[Error] POST '/zip' {ex} {message}")

    try:
        county = zip_info['county'].rsplit(' ', 1)[0]
        state = zip_info['state']
        _logger.info(f"State: {state}, County: {county}")
        if state == "NY":
            nyc_counties = ["Bronx", "Kings", "Queens", "Richmond"]
            if county in  nyc_counties:
                county = "New York"
            data = read_county_stats(state, county)[0]
        else:
            data = read_county_stats(state, county)[0]
        json_data = {"success": True, "message": data}
        del data
        gc.collect()
    except Exception as ex:
        _logger.warning(f"Endpoint: /zip --- POST --- {ex}")
        raise HTTPException(status_code=404,
                            detail=f"[Error] get '/zip' API: {ex}")

    return json_data
