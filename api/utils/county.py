import pandas as pd
from api.utils import convert_df_to_json


# Base URL for fetching data
base_url = "https://facts.csbs.org/covid-19/covid19_county.csv"


def read_county() -> pd.DataFrame:
    df = pd.read_csv(base_url)
    # df = df.apply(lambda x: x.astype(str).str.lower())
    # df = df[~(df["County Name"].isin(["unassigned", "unknown"]))]
    return df


def read_county_data():
    df = read_county()
    return convert_df_to_json(df)


if __name__ == "__main__":
    pass
