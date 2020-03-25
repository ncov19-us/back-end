import pandas as pd
from api.utils import reverse_states_map
from api.utils import convert_df_to_json


# Base URL for fetching data
base_url = "https://facts.csbs.org/covid-19/covid19_county.csv"


def read_county_data() -> pd.DataFrame:
    df = pd.read_csv(base_url)
    df = df.apply(lambda x: x.astype(str).str.lower())
    df = df[~(df["County Name"] == "unassigned")]
    return convert_df_to_json(df)


if __name__ == "__main__":
    pass
