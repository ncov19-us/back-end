import logging
from logging.handlers import TimedRotatingFileHandler
import pathlib
import os
import sys
from decouple import config


################################################################################
#                               Logging
################################################################################
PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)-12s — %(levelname)-8s —"
    "%(funcName)s:%(lineno)d — %(message)s"
)

CONSOLE_FORMATTER = logging.Formatter(
    "%(name)-12s: %(levelname)-8s %(message)s"
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


################################################################################
#                               Custom Exceptions
################################################################################
class DataReadingError(Exception):
    """DataReadingError exception used for sanity checking.
    """
    def __init__(self, *args):
        super(DataReadingError, self).__init__(*args)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"DataReadingError {self.message}"

        return "DataReadingError"


class DataValidationError(Exception):
    """DataValidationError exception used for sanity checking.
    """
    def __init__(self, *args):
        super(DataValidationError, self).__init__(*args)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"DataValidationError {self.message}"

        return "DataValidationError"


################################################################################
#                                  Configs
################################################################################
class Config:
    """
    Base config for Staging API
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    # Add MongoConnection
    MONGODB_CONNECTION_URI = config("MONGODB_CONNECTION_URI")

    # Add Collections here
    COLLECTION_STATE = "state"
    COLLECTION_COUNTY = "county"
    COLLECTION_TWITTER = "twitter"

    # JHU CSSE Daily Reports
    BASE_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/" \
               "master/csse_covid_19_data/csse_covid_19_daily_reports/"

    # JHU CSSE time series reports
    TIME_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/" \
               "master/csse_covid_19_data/csse_covid_19_time_series/" \
               "time_series_19-covid-Confirmed.csv"

    # NEWS API
    NEWS_API_KEY = config("NEWS_API_KEY")
    NEWS_API_URL = (
        f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    )

    # CVTRACK
    CVTRACK_URL = "https://covidtracking.com/api/us/daily"
    CVTRACK_STATES_URL = "https://covidtracking.com/api/states"

    TMP_URL = "https://coronavirus-19-api.herokuapp.com/countries/USA"

    # ADD DATA URLS
    COUNTY_URL = config("COUNTY_URL")
    STATE_CONFIRMED = config("STATE_CONFIRMED")
    STATE_DEATH = config("STATE_DEATH")
    NYT_STATE = config("NYT_STATE")

    DB_NAME = "covid"


    INFO = dict(
        {
            "title": "ncov19.us API",
            "description": (
                "API Support: ncov19us@gmail.com | "
                "URL: https://github.com/ncov19-us/back-end | "
                "[GNU GENERAL PUBLIC LICENSE]"
                "(https://github.com/ncov19-us/back-end/blob/master/LICENSE)"
                ),
        }
    )


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    DB_NAME = "covid"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True
    DB_NAME = "covid-staging"



def get_config():
    """Set default config to ProductionConfig unless STAGING environment
    is set to false on Linux `export STAGING=False` or Windows Powershell
    `$Env:STAGING="False"`. Using os.environ directly will throw errors
    if not set.

    For pytest, plesae use ProductionConfig
    """
    STAGING = os.getenv("STAGING") or "True"

    if STAGING == "False":
        return DevelopmentConfig()

    return ProductionConfig()


app_config = get_config()

print(f"[INFO] Config being used is: {app_config.__class__.__name__}")
