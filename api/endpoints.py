import os
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

# Starts the FastAPI Router to be used by the FastAPI app.
router = APIRouter()
tm = TwitterMongo("covid", "twitter", verbose=True)


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
        json_data = {"sucess": True, "message": data}
    except Exception as ex:
        json_data = {"sucess": False, "message": f"Error occurred: {ex}"}
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

    # if news.state == "US":
    #     json_data = get_us_news()
    #     return json_data
    try:
        state = reverse_states_map[news.state]
        json_data = get_state_topic_google_news(state, news.topic)
        json_data = {"sucess": True, "message": json_data}
    except Exception as ex:
        json_data = {"sucess": False, "message": f"Error occured {ex}"}
    return json_data


@router.get("/county")
def get_data() -> JSONResponse:
    """Get all US county data and return it as a big fat json string.

    :param: none.
    :return: JSONResponse
    """
    pass


@router.get("/stats")
def get_stats() -> JSONResponse:
    """Get overall tested, confirmed, and deaths stats from the database
    and return it as a json string. For the top bar.

    :param: none.
    :return: JSONResponse
    """
    return get_daily_stats()


@router.get("/twitter")
def get_twitter() -> str:
    """Fetch and return Twitter data from MongoDB connection.

    :param: none
    :return: str
    """

    doc = tm.get_tweet_by_state("US", verbose=True)
    username = doc["username"]
    full_name = doc["full_name"]
    tweets = doc["tweets"]

    # 2020-03-19 triage. lots of empty list at the end of tweets, filtering them out
    tweets = [*filter(None, tweets)]
    tweets = sorted(tweets, key=lambda i: i["created_at"], reverse=True)
    return tweets


class TwitterUser(BaseModel):
    state: str


@router.post("/twitter")
def post_twitter(twyuser: TwitterUser) -> str:
    """Fetch and return Twitter data from MongoDB connection.

    :param: none. Two letter state abbreviation.
    :return: str
    """
    doc = tm.get_tweet_by_state(twyuser.state)
    username = doc["username"]
    full_name = doc["full_name"]
    tweets = doc["tweets"]

    # 2020-03-19 triage. lots of empty list at the end of tweets, filtering them out
    tweets = [*filter(None, tweets)]
    tweets = sorted(tweets, key=lambda i: i["created_at"], reverse=True)
    return tweets
