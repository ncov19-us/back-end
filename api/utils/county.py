from typing import Dict
import pandas as pd
from api.utils import convert_df_to_json
from api.config import Config


def read_county() -> pd.DataFrame:
    """Read county data from COUNTY_URL

    :return: :pd.DataFrame: COUNTY_URL data ingested as a pandas Dataframe
    """
    df = pd.read_csv(Config.COUNTY_URL)
    # df = df.apply(lambda x: x.astype(str).str.lower())
    # df = df[~(df["County Name"].isin(["unassigned", "unknown"]))]
    return df


def read_county_data() -> Dict:
    """Read county data from COUNTY_URL

    :return: :Dict: COUNTY_URL as a python dictionary/json file.
    """
    df = read_county()
    return convert_df_to_json(df)


if __name__ == "__main__":
    pass
