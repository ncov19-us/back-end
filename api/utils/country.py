from typing import Any, Dict
import pandas as pd
import pycountry
# from api.utils import convert_df_to_json


# Country dictionary
country_dict = {
    "TD": "Chad",
    "AT": "Austria",
    "DE": "Germany",
    "KZ": "Kazakhstan",
    "AD": "Andorra",
    "IR": "Iran",
    "KN": "Saint Kitts and Nevis",
    "MG": "Madagascar",
    "JP": "Japan",
    "LT": "Lithuania",
    "CU": "Cuba",
    "CL": "Chile",
    "HT": "Haiti",
    "MX": "Mexico",
    "CR": "Costa Rica",
    "HN": "Honduras",
    "PE": "Peru",
    "PH": "Philippines",
    "BG": "Bulgaria",
    "LV": "Latvia",
    "SY": "Syria",
    "MV": "Maldives",
    "VE": "Venezuela",
    "NO": "Norway",
    "IS": "Iceland",
    "DM": "Dominica",
    "TG": "Togo",
    "CN": "China",
    "NP": "Nepal",
    "ME": "Montenegro",
    "SI": "Slovenia",
    "TR": "Turkey",
    "PG": "Papua New Guinea",
    "GA": "Gabon",
    "NZ": "New Zealand",
    "CV": "Cabo Verde",
    "CI": "Cote d'Ivoire",
    "AE": "United Arab Emirates",
    "DO": "Dominican Republic",
    "AZ": "Azerbaijan",
    "IN": "India",
    "BN": "Brunei",
    "MT": "Malta",
    "LC": "Saint Lucia",
    "PK": "Pakistan",
    "GW": "Guinea-Bissau",
    "NI": "Nicaragua",
    "HR": "Croatia",
    "MK": "North Macedonia",
    "BE": "Belgium",
    "MC": "Monaco",
    "BJ": "Benin",
    "UZ": "Uzbekistan",
    "HU": "Hungary",
    "GQ": "Equatorial Guinea",
    "BZ": "Belize",
    "SM": "San Marino",
    "GT": "Guatemala",
    "BB": "Barbados",
    "IE": "Ireland",
    "TH": "Thailand",
    "MU": "Mauritius",
    "ID": "Indonesia",
    "LR": "Liberia",
    "VN": "Vietnam",
    "ES": "Spain",
    "ZW": "Zimbabwe",
    "VA": "Holy See",
    "IQ": "Iraq",
    "EE": "Estonia",
    "TN": "Tunisia",
    "MA": "Morocco",
    "BR": "Brazil",
    "ZA": "South Africa",
    "DJ": "Djibouti",
    "ML": "Mali",
    "AO": "Angola",
    "BD": "Bangladesh",
    "LK": "Sri Lanka",
    "CA": "Canada",
    "ET": "Ethiopia",
    "US": "US",
    "RS": "Serbia",
    "BY": "Belarus",
    "SA": "Saudi Arabia",
    "MN": "Mongolia",
    "MZ": "Mozambique",
    "KE": "Kenya",
    "CH": "Switzerland",
    "CZ": "Czechia",
    "NL": "Netherlands",
    "SR": "Suriname",
    "GR": "Greece",
    "SE": "Sweden",
    "EC": "Ecuador",
    "AG": "Antigua and Barbuda",
    "LU": "Luxembourg",
    "NG": "Nigeria",
    "SN": "Senegal",
    "GH": "Ghana",
    "TT": "Trinidad and Tobago",
    "QA": "Qatar",
    "DK": "Denmark",
    "RU": "Russia",
    "GE": "Georgia",
    "GD": "Grenada",
    "MR": "Mauritania",
    "SG": "Singapore",
    "CY": "Cyprus",
    "GY": "Guyana",
    "KG": "Kyrgyzstan",
    "JO": "Jordan",
    "AR": "Argentina",
    "VC": "Saint Vincent and the Grenadines",
    "TL": "Timor-Leste",
    "PY": "Paraguay",
    "JM": "Jamaica",
    "BA": "Bosnia and Herzegovina",
    "BS": "Bahamas",
    "SO": "Somalia",
    "FI": "Finland",
    "BF": "Burkina Faso",
    "UA": "Ukraine",
    "CO": "Colombia",
    "OM": "Oman",
    "PL": "Poland",
    "LY": "Libya",
    "TZ": "Tanzania",
    "GM": "Gambia",
    "UG": "Uganda",
    "KH": "Cambodia",
    "MY": "Malaysia",
    "KW": "Kuwait",
    "EG": "Egypt",
    "AU": "Australia",
    "BH": "Bahrain",
    "AL": "Albania",
    "GN": "Guinea",
    "SV": "El Salvador",
    "IT": "Italy",
    "CM": "Cameroon",
    "NA": "Namibia",
    "SZ": "Eswatini",
    "RW": "Rwanda",
    "DZ": "Algeria",
    "ZM": "Zambia",
    "MD": "Moldova",
    "SD": "Sudan",
    "BO": "Bolivia",
    "PA": "Panama",
    "SC": "Seychelles",
    "IL": "Israel",
    "BT": "Bhutan",
    "RO": "Romania",
    "ER": "Eritrea",
    "LI": "Liechtenstein",
    "SK": "Slovakia",
    "AM": "Armenia",
    "FR": "France",
    "AF": "Afghanistan",
    "LB": "Lebanon",
    "FJ": "Fiji",
    "GB": "United Kingdom",
    "UY": "Uruguay",
    "CF": "Central African Republic",
    "PT": "Portugal",
    "KR": "Korea, South",
    "TW": "Taiwan*",
    "PS": "West Bank and Gaza",
}


def parse_df(metric_type: str) -> pd.DataFrame:
    """ Parse data in Johns Hopkins github csv file for the supported metric_type
    and return the dataframe to people.

    :param: :str: :metric_type: Currently only confirmed or death supported
    :return: :pd.DataFrame: dataframe of the queried data.
    """
    if metric_type.startswith("confirmed"):
        metric_type = "confirmed"
    elif metric_type.startswith("death"):
        metric_type = "deaths"
    else:
        raise ValueError(f"{metric_type} metric type not supported")

    url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{metric_type}_global.csv"
    df = pd.read_csv(url)
    return df


def get_country_stats(country_alpha: str, metric_type: str) -> pd.DataFrame:
    """ Find the metric type data from the Johns Hopkins github csv file for
    a specific country and returns to the dataframe.

    :param: :country_alpha: :str: country alpha2 code.
    :param: :metric_type: :str: currently only confirmed or death supported
    :return: :pd.DataFrame: dataframe of the queried data.
    """

    country_alpha = country_alpha.upper()
    metric_type = metric_type.lower()

    df = parse_df(metric_type=metric_type)

    if country_alpha not in country_dict:
        raise ValueError(f"{country_alpha} not found in our dictionary.")
    country = country_dict[country_alpha]

    df = df[df["Country/Region"] == country]
    df = df.drop(columns=["Lat", "Long", "Country/Region", "Province/State"])
    df = df.sum(axis=0).to_frame().reset_index()
    df = df.rename(columns={0: metric_type.title()})
    df = df.reset_index(drop=True)
    df = df.rename(columns={"index": "Date"})

    return df


def read_country_data(country_alpha: str) -> Dict:
    """ Find both confirmed and deaths data from the Johns Hopkins github csv 
    file and returns to people.

    :param: :country_alpha: :str: country alpha2 code.
    :return: :Dict: json file.
    """
    df1 = get_country_stats(country_alpha, metric_type="confirmed")
    df2 = get_country_stats(country_alpha, metric_type="deaths")
    merge = pd.merge(df1, df2, on="Date")

    # return convert_df_to_json(merge)
    # return pd.DataFrame.to_json(merge, orient="records")
    return pd.DataFrame.to_dict(merge, orient="records")


if __name__ == "__main__":
    df = read_country_data("KR")
    print(df)
