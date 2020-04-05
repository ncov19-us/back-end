from typing import Dict
import pandas as pd
from api.config import Config
from api.utils import reverse_states_map


def read_county_data() -> pd.DataFrame:
    """Read county data from COUNTY_URL, lower all county and state names.
    Also change spaces to underscores for Pydantic to do type enforcement.

    :return: :Dict: COUNTY_URL as a python dictionary/json file.
    """
    df = pd.read_csv(Config.COUNTY_URL)
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(" ", "_")
    df = pd.DataFrame.to_dict(df, orient="records")
    return df


def read_county_stats(state: str, county: str) -> pd.DataFrame:
    
    try:
        df = pd.read_csv(Config.COUNTY_URL)
        deaths = pd.read_csv(Config.STATE_DEATH)
    except:
        raise ValueError(
            f"Data reading error State: {state}, and County: {county}."
        )
    
    try:
        df.columns = map(str.lower, df.columns)
        df.columns = df.columns.str.replace(" ", "_")

        # used data source 2 for new death number
        deaths = deaths[deaths['Province_State'] == reverse_states_map[state]]
        deaths = deaths[deaths['Admin2'] == county]
        deaths = deaths.iloc[:, 12:].diff(axis=1).iloc[:, -1].values[0]    
        
        df = df[df["state_name"] == reverse_states_map[state]]
        # df = df.query(f"county_name == '{county}'")
        df = df[df["county_name"] == county]
        df.new_death.iloc[0] = deaths
        df = pd.DataFrame.to_dict(df, orient="records")
        if len(df) == 0:
            raise
    except:
        raise ValueError(
            f"Can't find State: {state}, and County: {county} combination."
        )
    return df


if __name__ == "__main__":
    pass
