import pandas as pd
from typing import Any, Dict


# Base URL for fetching data
jhu_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"


def read_country_data() -> Dict[str, Any]:
    """Read the data from jhu_url and parse
    """
    df = pd.read_csv(jhu_url)
    
    df = df[df["Country/Region"].isin(["US", "Korea, South", "Italy"])]
    # Have to use '//' to prepresent '/' here. Thanks Python!
    # But still not working :(
    # df.rename(columns={'Country//Region': "Date"}, inplace=True)
    df = df.drop(["Province/State", "Lat", "Long"], axis=1)
    df = df.set_index("Country/Region").transpose()
    df.rename(columns={'Korea, South': "South Korea"}, inplace=True)
    df = pd.DataFrame.to_json(df, orient="records")

    return df


if __name__ == "__main__":
    df = read_country_data()