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
    df = pd.read_csv(Config.COUNTY_URL)
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(" ", "_")
    try:
        df = df[df["state_name"] == reverse_states_map[state]]
        # df = df.query(f"county_name == '{county}'")
        df = df[df["county_name"] == county]
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
