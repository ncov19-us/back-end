from typing import Dict
import pandas as pd
import zipcodes
from api.config import DataReadingError, DataValidationError
from api.config import app_config
from api.utils import reverse_states_map


def read_county_stats_zip_ny(zipcode: str) -> Dict:
    """Return stats for New York State zip_codes
    """

    zip_info = zipcodes.matching(str(zipcode))[0]
    county = zip_info["county"].rsplit(" ", 1)[0]
    state = zip_info["state"]

    try:
        deaths = pd.read_csv(app_config.STATE_DEATH)
        confirmed_df = pd.read_csv(app_config.STATE_CONFIRMED)
    except:
        raise DataReadingError(
            f"Data reading error State: {state}, and County: {county}."
        )

    try:
        confirmed_df = confirmed_df[
            confirmed_df["Province_State"] == reverse_states_map[state]
        ]
        confirmed_df = confirmed_df[confirmed_df["Admin2"] == county]

        confirmed = confirmed_df.iloc[:, -1]
        new_confirmed = (
            confirmed_df.iloc[:, 12:]
            .astype("int32")
            .diff(axis=1)
            .iloc[:, -1]
            .values[0]
        )

        # used data source 2 for new death number
        deaths = deaths[deaths["Province_State"] == reverse_states_map[state]]
        deaths = deaths[deaths["Admin2"] == county]
        # 4/15/20: force cast into int before diff as pd sometimes read as
        # float and throws nan.
        death = deaths.iloc[:, -1]
        new_death = (
            deaths.iloc[:, 12:]
            .astype("int32")
            .diff(axis=1)
            .iloc[:, -1]
            .values[0]
        )
        try:
            fatality_rate = int(death) / int(confirmed)
        except:  # pylint: disable=W0702
            fatality_rate = 0

        data = {
            "county_name": county,
            "state_name": reverse_states_map[state],
            "confirmed": int(confirmed),
            "new": int(new_confirmed),
            "death": int(death),
            "new_death": int(new_death),
            "fatality_rate": f"{fatality_rate}%",
            "latitude": float(zip_info["lat"]),
            "longitude": float(zip_info["long"]),
            "last_update": str("2020-04-17 19:50 EDT"),
        }
        print(data)
        # data = json.dumps(data)
        # print(data)
    except:
        raise DataValidationError(
            f"Can't find State: {state}, and County: {county} combination."
        )
    return data


if __name__ == "__main__":
    pass
