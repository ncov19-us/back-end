import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib
import os
import sys
from decouple import config
import tweepy

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —" "%(funcName)s:%(lineno)d — %(message)s"
)

LOG_DIR = PACKAGE_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "api.log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    console_handler.setLevel(logging.DEBUG)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
    file_handler.setFormatter(FORMATTER)
    file_handler.setLevel(logging.WARNING)
    return file_handler


def get_logger(*, logger_name):
    """
    Get logger with prepared handlers.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SERVER_PORT = 8000
    COLLECTION_STATE = "state"
    COLLECTION_COUNTY = "county"
    COLLECTION_TWITTER = "twitter"
    # JHU CSSE Daily Reports
    BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
    # JHU CSSE time series reports
    TIME_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    NEWS_API_KEY = config("NEWS_API_KEY")
    NEWS_API_URL = (
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    )
    CVTRACK_URL = "https://covidtracking.com/api/us/daily"
    CVTRACK_STATES_URL = "https://covidtracking.com/api/states"
    TMP_URL = "https://coronavirus-19-api.herokuapp.com/countries/USA"
    COUNTY_URL = config("COUNTY_URL")


class ProductionConfig(Config):
    DEBUG = False
    DB_NAME = "covid"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DB_NAME = "covid-staging"
