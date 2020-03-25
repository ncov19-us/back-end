import requests
from api.config import Config
from typing import Dict


def get_daily_stats() -> Dict:
    # initialize the variables so it doesnt crash if both api call failed

    confirmed, todays_confirmed, deaths, todays_deaths, recovered = 0, 0, 0, 0, 0

    try:
        data1 = requests.get(url=Config.CVTRACK_URL).json()[0]
        tested = data1["posNeg"]
        tested_positive = data1["positive"]
        tested_negative = data1["negative"]
        hospitalized = data1["hospitalized"]
    except:
        tested = 0

    try:
        data2 = requests.get(url=Config.TMP_URL).json()

        confirmed = data2["cases"]
        todays_confirmed = data2["todayCases"]
        deaths = data2["deaths"]
        todays_deaths = data2["todayDeaths"]
        critical = data2["critical"]
        active = data2["active"]
    except:
        confirmed, todays_confirmed, deaths, todays_deaths, recovered = (0, 0, 0, 0, 0)

    stats = {
        "tested": tested,
        "confirmed": confirmed,
        "todays_confirmed": todays_confirmed,
        "deaths": deaths,
        "todays_deaths": todays_deaths,
    }

    return stats
