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

    data = pd.read_csv(config_.NYT_STATE)
    data = data[data['state']==state]
    data = data[['date', 'cases', 'deaths']]
    data.columns = ['Date', 'Confirmed', 'Deaths']
    data = data.fillna(0)
    dict_data = pd.DataFrame.to_dict(data, orient="records")

    del data
    gc.collect()

    return dict_data