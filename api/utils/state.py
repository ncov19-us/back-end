import gc
from typing import Dict
import pandas as pd
from api.config import config_
from api.utils import reverse_states_map


def read_states(state:str) -> pd.DataFrame:
    """read date, confirmed, and death info of a state and return it as
    a dictionary
    """
    
    state = reverse_states_map[state]

    data = pd.read_csv(config_.STATE_CONFIRMED)
    data = data[data['Province_State'] == state]

    deaths = pd.read_csv(config_.STATE_DEATH)
    deaths = deaths[deaths['Province_State'] == state]

    # HARD CODE:
    if  state == "Montana":
        # fix death
        pass
    elif state == "New Hampshire":
        row  = data[data['Admin2'] == 'Hillsborough'].transpose().replace(to_replace=0, method='ffill').transpose()
        data[data['Admin2']=='Hillsborough'] = row
        # fix death and confirmed
        pass
    elif state == "Hawaii":
        # fix death
        pass
    elif state == "New Jersey":
        # fix death
        pass
    elif state == "North Carolina":
        # fix death
        pass

    data = pd.DataFrame(data.aggregate('sum')[11:], columns=['Confirmed'])

    deaths = pd.DataFrame(deaths.aggregate('sum')[12:])

    data['Deaths'] = deaths

    data = data.reset_index()
    data.columns = ['Date', 'Confirmed', 'Deaths']
    data = data.fillna(0)
    # print(data.head())
    # print(data.tail())
    data = pd.DataFrame.to_dict(data, orient="records")

    del deaths
    gc.collect()

    return data