import gc
from typing import Dict
import requests
import pandas as pd
from api.config import DataReadingError, DataValidationError
from api.config import app_config
from api.config import get_logger
from api.utils import reverse_states_map


_logger = get_logger(logger_name=__name__)


def get_daily_stats() -> Dict:
    """Get daily stats for a specific state, including tested, confirmed,
    todays_confirmed, deaths, and todays_deaths. Everything is initialized
    at zero.

    :params: :str: state. the state to look up.
    :return: :Dict: {"tested": str,
                     "todays_tested": str,
                     "confirmed": str,
                     "todays_confirmed": str,
                     "deaths": str,
                     "todays_deaths: str}
    """
    # initialize the variables so it doesnt crash if both api call failed

    tested, todays_tested, confirmed = 0, 0, 0
    todays_confirmed, deaths, todays_deaths = 0, 0, 0

    try:
        data2 = requests.get(url=app_config.TMP_URL).json()
        confirmed = data2["cases"]
        todays_confirmed = data2["todayCases"]
        deaths = data2["deaths"]
        todays_deaths = data2["todayDeaths"]

        del data2
        gc.collect()
    except DataReadingError as ex:
        _logger.error(f"stats.get_daily_stats {ex}")
        confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0

    try:
        # covidtracking api
        data = requests.get(url=app_config.CVTRACK_URL).json()
        curr = data[0]
        prev = data[1]
        # 2020-10-10 updated for new api schema
        tested = curr["totalTestResults"]
        todays_tested = curr["totalTestResults"] - prev["totalTestResults"]
        confirmed = curr["positive"]
        todays_confirmed = curr["positive"] - prev["positive"]
        deaths = curr["death"]
        todays_deaths = curr["death"] - prev["death"]

        del data
        gc.collect()
    except DataReadingError as ex:
        _logger.error(f"stats.get_daily_stats {ex}")
        tested = 0

    stats = {
        "tested": tested,
        "todays_tested": todays_tested,
        "confirmed": confirmed,
        "todays_confirmed": todays_confirmed,
        "deaths": deaths,
        "todays_deaths": todays_deaths,
    }
    print(stats)

    ###################################################################
    #                     Sanity Check
    ###################################################################
    if int(todays_tested) >= int(tested):
        raise DataValidationError("get /stats tested validation error")

    if int(todays_confirmed) >= int(confirmed):
        raise DataValidationError("get /stats confirmed validation error")

    if (int(confirmed) > int(tested)) or (int(deaths) > int(confirmed)):
        raise DataValidationError("get /stats comparison validation error")

    return stats


def get_daily_state_stats(state: str) -> Dict:
    """Get daily stats for a specific state, including tested, confirmed,
    todays_confirmed, deaths, and todays_deaths. Everything is initialized
    at zero.

    :params: :str: state. the state to look up.
    :return: :Dict: {"tested": str,
                     "todays_tested": str,
                     "confirmed": str,
                     "todays_confirmed": str,
                     "deaths": str,
                     "todays_deaths: str}
    """
    # initialize the variables so it doesnt crash if both api call failed

    tested, todays_tested, confirmed = 0, 0, 0
    todays_confirmed, deaths, todays_deaths = 0, 0, 0

    # Get tested data
    URL = app_config.CVTRACK_STATES_URL
    response = requests.get(url=URL)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            try:
                data = [d for d in data if d["state"] == state]
                curr = data[0]
                prev = data[1]
                todays_tested = (
                    curr["totalTestResults"] - prev["totalTestResults"]
                )
                tested = curr["totalTestResults"]
            except DataReadingError as ex:
                raise DataReadingError(f"error getting tested data {ex}")
        else:
            tested, todays_tested = 0, 0
    else:
        raise DataReadingError("get_daily_state_stats data reading error")

    # Get confirmed and deaths data
    try:
        base_url = app_config.COUNTY_URL
        df = pd.read_csv(base_url)
        df = df[df["State Name"] == reverse_states_map[state]]
        grouped = df.groupby(["State Name"])
        confirmed = grouped["Confirmed"].sum().values[0].astype(str)
        todays_confirmed = grouped["New"].sum().values[0].astype(str)
        deaths = grouped["Death"].sum().values[0].astype(str)
        todays_deaths = grouped["New Death"].sum().values[0].astype(str)
    except DataReadingError as ex:
        raise DataReadingError(f"get_daily_state_stats parsing error {ex}")

    stats = {
        "tested": tested,
        "todays_tested": todays_tested,
        "confirmed": confirmed,
        "todays_confirmed": todays_confirmed,
        "deaths": deaths,
        "todays_deaths": todays_deaths,
    }

    ###################################################################
    #                     Sanity Check
    ###################################################################
    if int(todays_tested) >= int(tested):
        raise DataValidationError("/stats tested number validation error")

    if int(todays_confirmed) >= int(confirmed):
        raise DataValidationError("/stats confirmed number validation error")

    if (int(confirmed) > int(tested)) or (int(deaths) > int(confirmed)):
        raise DataValidationError("/stats numbers comparison validation error")

    del df, data
    gc.collect()

    return stats
