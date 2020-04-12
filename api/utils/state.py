import gc
from typing import Dict
import pandas as pd
from api.config import app_config
from api.config import DataReadingError, DataValidationError
from api.utils import reverse_states_map


def read_states(state:str) -> Dict:
    """read date, confirmed, and death info of a state and return it as
    a dictionary
    """
    
    state = reverse_states_map[state]

    try:
        data = pd.read_csv(app_config.NYT_STATE)
        data = data[data['state']==state]
        data = data[['date', 'cases', 'deaths']]
        data.columns = ['Date', 'Confirmed', 'Deaths']
        data = data.fillna(0)
        dict_data = pd.DataFrame.to_dict(data, orient="records")

        del data
        gc.collect()
    except:
        raise DataReadingError("error reading data")

    return dict_data
