import pandas as pd


# Base URL for fetching data
base_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"


def read_country_data() -> pd.DataFrame:
    df = pd.read_csv(base_url)
    df = df[df["Country/Region"].isin(["US", "Korea, South", "Italy"])]
    df = pd.DataFrame.to_json(df, orient="records")
    return df


if __name__ == "__main__":
    df = read_country_data()
    print(df)