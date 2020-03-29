import requests
from api.config import Config
from typing import Dict
from api.utils import reverse_states_map
import pandas as pd
import json


def get_daily_stats() -> Dict:
    # initialize the variables so it doesnt crash if both api call failed

    confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0

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
        confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0

    stats = {
        "tested": tested,
        "confirmed": confirmed,
        "todays_confirmed": todays_confirmed,
        "deaths": deaths,
        "todays_deaths": todays_deaths,
    }

    return stats


def get_daily_state_stats(state: str) -> Dict:
    # initialize the variables so it doesnt crash if both api call failed

    tested, confirmed, todays_confirmed, deaths, todays_deaths = 0, 0, 0, 0, 0
    URL = Config.CVTRACK_STATES_URL + f"/daily?state={state}"

    response = requests.get(url=URL)
    # print(response.json())
    if response.status_code == 200:
        # covidtracking api throws error json if request error {'error': }
        if type(response.json()) is list:
            try:
                data = response.json()
                curr = data[0]
                tested = curr["totalTestResults"]
            except:
                return {"error": "get_daily_state_stats API parsing error."}

        base_url = "https://facts.csbs.org/covid-19/covid19_county.csv"
        df = pd.read_csv(base_url)
        df = df[df["State Name"] == reverse_states_map[state]]
        grouped = df.groupby(["State Name"])
        confirmed = grouped["Confirmed"].sum().values[0].astype(str)
        todays_confirmed = grouped["New"].sum().values[0].astype(str)
        death = grouped["Death"].sum().values[0].astype(str)
        todays_death = grouped["New Death"].sum().values[0].astype(str)

    stats = {
        "tested": tested,
        "confirmed": confirmed,
        "todays_confirmed": todays_confirmed,
        "deaths": deaths,
        "todays_deaths": todays_deaths,
    }

    return stats
