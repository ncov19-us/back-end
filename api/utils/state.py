import gc
import json
from typing import Dict
from datetime import datetime

import pandas as pd
from mongoengine import connect, disconnect

from api.config import app_config
from api.config import DataReadingError
from api.utils import reverse_states_map
from api.utils import County


def read_states(state: str) -> Dict:
    """read date, confirmed, and death info of a state and return it as
    a dictionary
    """

    state = reverse_states_map[state]

    try:
        data = pd.read_csv(app_config.NYT_STATE)
        data = data[data['state'] == state]
        data = data[['date', 'cases', 'deaths']]
        data.columns = ['Date', 'Confirmed', 'Deaths']
        data = data.fillna(0)
        dict_data = pd.DataFrame.to_dict(data, orient="records")

        del data
        gc.collect()
    except:
        raise DataReadingError("error reading data")

    return dict_data


def read_states_mongo(state: str) -> Dict:
    """read date, confirmed, and death info
    """
    URI = app_config.MONGODB_CONNECTION_URI
    connect(host=URI)
    counties = County.objects(state=state)
    # county = json.loads(county.to_json())

    confirmed = [sum(county.stats[i]['confirmed'] for county in counties)\
                for i in range(len(counties[0].stats))]
    deaths = [sum(county.stats[i]['confirmed'] for county in counties)\
                for i in range(len(counties[0].stats))]
    dates = [stat['last_updated'] for stat in counties[0].stats]

    disconnect()

    return data