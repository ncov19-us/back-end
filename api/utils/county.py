from typing import Dict
import pandas as pd
from api.config import Config


def read_county_data() -> Dict:
    """Read county data from COUNTY_URL, lower all county and state names.
    Also change spaces to underscores for Pydantic to do type enforcement.

    :return: :Dict: COUNTY_URL as a python dictionary/json file.
    """
    df = pd.read_csv(Config.COUNTY_URL)
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(' ', '_')
    df = pd.DataFrame.to_dict(df, orient="records")
    return df


if __name__ == "__main__":
    pass
