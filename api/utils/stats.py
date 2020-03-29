import requests
from api.config import Config
from typing import Dict


def get_daily_stats() -> Dict:
    # initialize the variables so it doesnt crash if both api call failed

    confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0

    try:
        data2 = requests.get(url=Config.TMP_URL).json()

        confirmed = data2["cases"]
        todays_confirmed = data2["todayCases"]
        deaths = data2["deaths"]
        todays_deaths = data2["todayDeaths"]
        # critical = data2["critical"]
        # active = data2["active"]
    except:
        confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0

    try:
        # covidtracking api
        data = requests.get(url=Config.CVTRACK_URL).json()
        curr = data[0]
        prev = data[1]
        tested = curr["posNeg"]
        todays_tested = curr["totalTestResults"] - prev["totalTestResults"]
        confirmed = curr["positive"]
        todays_confirmed = curr["positive"] - prev["positive"]
        deaths = curr["death"]
        todays_deaths = curr["death"] - prev["death"]
        # tested_positive = curr["positive"]
        # tested_negative = data1["negative"]
        # hospitalized = data1["hospitalized"]
    except:
        tested = 0

    stats = {
        "tested": tested,
        "todays_tested": todays_tested,
        "confirmed": confirmed,
        "todays_confirmed": todays_confirmed,
        "deaths": deaths,
        "todays_deaths": todays_deaths,
    }

    return stats


def get_daily_state_stats(state: str) -> Dict:
    # initialize the variables so it doesnt crash if both api call failed

    tested, confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0, 0
    URL = Config.CVTRACK_STATES_URL+f"/daily?state={state}"

    response = requests.get(url=URL)
    # print(response.json())
    if response.status_code == 200:
        # covidtracking api throws error json if request error {'error': }
        if type(response.json()) is list:
            try:
                data = response.json()
                curr = data[0]
                prev = data[1]
                tested = curr['totalTestResults']
                todays_tested = curr['totalTestResults'] - prev['totalTestResults']
                confirmed = curr['positive']
                todays_confirmed = curr['positive'] - prev['positive']
                deaths = curr['death']
                todays_deaths = curr['death'] - prev['death']

            except:
                return {"error": "get_daily_state_stats API parsing error."}

    stats = {
        "tested": tested,
        "todays_tested": todays_tested,
        "confirmed": confirmed,
        "todays_confirmed": todays_confirmed,
        "deaths": deaths,
        "todays_deaths": todays_deaths,
    }

    return stats