from typing import Dict
import pandas as pd
from api.config import Config
from api.utils import reverse_states_map


def read_states(state:str) -> pd.DataFrame:
    """read date, confirmed, and death info of a state and return it as
    a dictionary
    """
    
    state = reverse_states_map[state]

    data = pd.read_csv(Config.STATE_CONFIRMED)
    data = data[data['FIPS'] < 79999]
    deaths = pd.read_csv(Config.STATE_DEATH)
    deaths = deaths[deaths['FIPS'] < 79999]

    data = data[data['Province_State'] == state]
    data = pd.DataFrame(data.aggregate('sum')[11:], columns=['Confirmed'])

    deaths = deaths[deaths['Province_State'] == state]
    deaths = pd.DataFrame(deaths.aggregate('sum')[12:])

    data['Deaths'] = deaths
    data = data.reset_index()
    data.columns = ['Date', 'Confirmed', 'Deaths']
    data = data.fillna(0)
    print(data.head())
    print(data.tail())
    data = pd.DataFrame.to_dict(data, orient="records")

    return data