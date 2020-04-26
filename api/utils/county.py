from typing import Dict
import pandas as pd
from cachetools import cached, TTLCache

from api.config import DataReadingError, DataValidationError
from api.config import app_config
from api.utils import reverse_states_map


def read_county_data() -> pd.DataFrame:
    """Read county data from COUNTY_URL, lower all county and state names.
    Also change spaces to underscores for Pydantic to do type enforcement.

    :return: :Dict: COUNTY_URL as a python dictionary/json file.
    """
    df = pd.read_csv(app_config.COUNTY_URL)
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(" ", "_")
    df = pd.DataFrame.to_dict(df, orient="records")

    return df


@cached(cache=TTLCache(maxsize=1, ttl=3600))
def ingest_county_data(*, url: str) -> pd.DataFrame:
    """Read county data from COUNTY_URL, lower all county and state names.
    Also change spaces to underscores for Pydantic to do type enforcement.

    :return: :Dict: COUNTY_URL as a python dictionary/json file.
    """

    df = pd.read_csv(url)
    df.columns = map(str.lower, df.columns)
    df.columns = df.columns.str.replace(" ", "_")

    df = wrangle_df(df=df)
    return df


def wrangle_df(*, df: pd.DataFrame) -> pd.DataFrame:
    """combine -- entries together, specifically for Harris County (Houston), TX
    and Wayne County (Detroit), MI
    """

    harris = df[
        df["county_name"].str.contains("Harris.*Houston", regex=True)
        & (df["state_name"] == "Texas")
    ]
    harris = harris.reset_index(drop=True)
    harris.loc[0, "county_name"] = "Harris"
    harris.loc[0, "confirmed"] += harris.loc[1, "confirmed"]
    harris.loc[0, "new"] += harris.loc[1, "new"]
    harris.loc[0, "death"] += harris.loc[1, "death"]
    harris.loc[0, "new_death"] += harris.loc[1, "new_death"]
    harris.loc[
        0, "fatality_rate"
    ] = f"{harris.loc[0, 'death']/harris.loc[0, 'confirmed']:.2f}%"
    df = df.append(harris.iloc[0], ignore_index=True)

    wayne = df[
        df["county_name"].str.contains("Wayne.*Detroit", regex=True)
        & (df["state_name"] == "Michigan")
    ]
    wayne = wayne.reset_index(drop=True)
    wayne.loc[0, "county_name"] = "Wayne"
    wayne.loc[0, "confirmed"] += wayne.loc[1, "confirmed"]
    wayne.loc[0, "new"] += wayne.loc[1, "new"]
    wayne.loc[0, "death"] += wayne.loc[1, "death"]
    wayne.loc[0, "new_death"] += wayne.loc[1, "new_death"]
    wayne.loc[
        0, "fatality_rate"
    ] = f"{wayne.loc[0, 'death']/wayne.loc[0, 'confirmed']:.2f}%"
    df = df.append(wayne.iloc[0], ignore_index=True)

    return df


def read_county_stats(state: str, county: str) -> Dict:

    try:
        df = ingest_county_data(url=app_config.COUNTY_URL)
    except:
        raise DataReadingError(
            f"Data reading error State: {state}, and County: {county}."
        )

    # 2020-04-22 patch counties
    if (state == "WA") and (county in ["Benton", "Franklin"]):
        county = "Benton and Franklin"

    if (state == "MA") and (county in ["Dukes", "Nantucket"]):
        county = "Dukes and Nantucket"

    # 2020-04-26 patch territories and districts
    territories = ["DC", "GU", "AS", "PR", "MP"]

    # Fetch state data
<<<<<<< HEAD
    full_state_name = state
=======
>>>>>>> 8661e05... chore: merge conflict, fix: zip codes for territories, fix: zip code error response message (#62)
    try:
        full_state_name = reverse_states_map[state]
        df = df[df["state_name"] == full_state_name]
        if len(df) == 0:
            raise DataValidationError(
                f"No records found for {full_state_name} in our database."
            )
    except:
        raise DataReadingError(f"Can't find {full_state_name} in our database.")

    # Now fetch county data
    try:
        if state in territories:
<<<<<<< HEAD
            df = df.reset_index(drop=True)
            df.loc[0, "county_name"] = full_state_name
            # 2020-04-26 pandanmic
            # df["county_name"] == full_state_name
=======
            df["county_name"] = full_state_name
>>>>>>> 8661e05... chore: merge conflict, fix: zip codes for territories, fix: zip code error response message (#62)
        else:
            df = df[df["county_name"] == county]
        if len(df) == 0:
            raise DataValidationError(
                f"No records found for {full_state_name} in our database."
            )
    except:
        raise DataValidationError(
<<<<<<< HEAD
            f"Can't find State: {full_state_name},"
            f" and County: {county} combination."
=======
            f"Can't find State: {full_state_name}, and County: {county} combination."
>>>>>>> 8661e05... chore: merge conflict, fix: zip codes for territories, fix: zip code error response message (#62)
        )
    df = pd.DataFrame.to_dict(df, orient="records")
    return df


if __name__ == "__main__":
    pass
