from datetime import datetime
from decouple import config
import pandas as pd
from mongoengine import *

# from api.config import MONGODB_CONNECTION_URI
import pymongo
import pprint

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
    "BU": "Burma",
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
    "BI": "Burundi",
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
    "BW": "Botswana",
    "CG": "Congo (Brazzaville)",
    "KV": "Kosovo",
    "CD": "Congo (Kinshasa)",
    "LA": "Laos",
}

reverse_country_map = {}
for k, v in country_dict.items():
    reverse_country_map[v] = k

# print(reverse_country_map)

states = [
    {
        "state": "Alabama",
        "latitude": 32.806671,
        "longitude": -86.791130,
        "state_abbrv": "AL",
    },
    {
        "state": "Alaska",
        "latitude": 61.370716,
        "longitude": -152.404419,
        "state_abbrv": "AK",
    },
    {
        "state": "Arizona",
        "latitude": 33.729759,
        "longitude": -111.431221,
        "state_abbrv": "AZ",
    },
    {
        "state": "Arkansas",
        "latitude": 34.969704,
        "longitude": -92.373123,
        "state_abbrv": "AR",
    },
    {
        "state": "California",
        "latitude": 36.116203,
        "longitude": -119.681564,
        "state_abbrv": "CA",
    },
    {
        "state": "Colorado",
        "latitude": 39.059811,
        "longitude": -105.311104,
        "state_abbrv": "CO",
    },
    {
        "state": "Connecticut",
        "latitude": 41.597782,
        "longitude": -72.755371,
        "state_abbrv": "CT",
    },
    {
        "state": "Delaware",
        "latitude": 39.318523,
        "longitude": -75.507141,
        "state_abbrv": "DE",
    },
    {
        "state": "District of Columbia",
        "latitude": 38.897438,
        "longitude": -77.026817,
        "state_abbrv": "DC",
    },
    {
        "state": "Florida",
        "latitude": 27.766279,
        "longitude": -81.686783,
        "state_abbrv": "FL",
    },
    {
        "state": "Georgia",
        "latitude": 33.040619,
        "longitude": -83.643074,
        "state_abbrv": "GA",
    },
    {
        "state": "Hawaii",
        "latitude": 21.094318,
        "longitude": -157.498337,
        "state_abbrv": "HI",
    },
    {
        "state": "Idaho",
        "latitude": 44.240459,
        "longitude": -114.478828,
        "state_abbrv": "ID",
    },
    {
        "state": "Illinois",
        "latitude": 40.349457,
        "longitude": -88.986137,
        "state_abbrv": "IL",
    },
    {
        "state": "Indiana",
        "latitude": 39.849426,
        "longitude": -86.258278,
        "state_abbrv": "IN",
    },
    {
        "state": "Iowa",
        "latitude": 42.011539,
        "longitude": -93.210526,
        "state_abbrv": "IA",
    },
    {
        "state": "Kansas",
        "latitude": 38.526600,
        "longitude": -96.726486,
        "state_abbrv": "KS",
    },
    {
        "state": "Kentucky",
        "latitude": 37.668140,
        "longitude": -84.670067,
        "state_abbrv": "KY",
    },
    {
        "state": "Louisiana",
        "latitude": 31.169546,
        "longitude": -91.867805,
        "state_abbrv": "LA",
    },
    {
        "state": "Maine",
        "latitude": 44.693947,
        "longitude": -69.381927,
        "state_abbrv": "ME",
    },
    {
        "state": "Maryland",
        "latitude": 39.063946,
        "longitude": -76.802101,
        "state_abbrv": "MD",
    },
    {
        "state": "Massachusetts",
        "latitude": 42.230171,
        "longitude": -71.530106,
        "state_abbrv": "MA",
    },
    {
        "state": "Michigan",
        "latitude": 43.326618,
        "longitude": -84.536095,
        "state_abbrv": "MI",
    },
    {
        "state": "Minnesota",
        "latitude": 45.694454,
        "longitude": -93.900192,
        "state_abbrv": "MN",
    },
    {
        "state": "Mississippi",
        "latitude": 32.741646,
        "longitude": -89.678696,
        "state_abbrv": "MS",
    },
    {
        "state": "Missouri",
        "latitude": 38.456085,
        "longitude": -92.288368,
        "state_abbrv": "MO",
    },
    {
        "state": "Montana",
        "latitude": 46.921925,
        "longitude": -110.454353,
        "state_abbrv": "MT",
    },
    {
        "state": "Nebraska",
        "latitude": 41.125370,
        "longitude": -98.268082,
        "state_abbrv": "NE",
    },
    {
        "state": "Nevada",
        "latitude": 38.313515,
        "longitude": -117.055374,
        "state_abbrv": "NV",
    },
    {
        "state": "New Hampshire",
        "latitude": 43.452492,
        "longitude": -71.563896,
        "state_abbrv": "NH",
    },
    {
        "state": "New Jersey",
        "latitude": 40.298904,
        "longitude": -74.521011,
        "state_abbrv": "NJ",
    },
    {
        "state": "New Mexico",
        "latitude": 34.840515,
        "longitude": -106.248482,
        "state_abbrv": "NM",
    },
    {
        "state": "New York",
        "latitude": 42.165726,
        "longitude": -74.948051,
        "state_abbrv": "NY",
    },
    {
        "state": "North Carolina",
        "latitude": 35.630066,
        "longitude": -79.806419,
        "state_abbrv": "NC",
    },
    {
        "state": "North Dakota",
        "latitude": 47.528912,
        "longitude": -99.784012,
        "state_abbrv": "ND",
    },
    {
        "state": "Ohio",
        "latitude": 40.388783,
        "longitude": -82.764915,
        "state_abbrv": "OH",
    },
    {
        "state": "Oklahoma",
        "latitude": 35.565342,
        "longitude": -96.928917,
        "state_abbrv": "OK",
    },
    {
        "state": "Oregon",
        "latitude": 44.572021,
        "longitude": -122.070938,
        "state_abbrv": "OR",
    },
    {
        "state": "Pennsylvania",
        "latitude": 40.590752,
        "longitude": -77.209755,
        "state_abbrv": "PA",
    },
    {
        "state": "Rhode Island",
        "latitude": 41.680893,
        "longitude": -71.511780,
        "state_abbrv": "RI",
    },
    {
        "state": "South Carolina",
        "latitude": 33.856892,
        "longitude": -80.945007,
        "state_abbrv": "SC",
    },
    {
        "state": "South Dakota",
        "latitude": 44.299782,
        "longitude": -99.438828,
        "state_abbrv": "SD",
    },
    {
        "state": "Tennessee",
        "latitude": 35.747845,
        "longitude": -86.692345,
        "state_abbrv": "TN",
    },
    {
        "state": "Texas",
        "latitude": 31.054487,
        "longitude": -97.563461,
        "state_abbrv": "TX",
    },
    {
        "state": "Utah",
        "latitude": 40.150032,
        "longitude": -111.862434,
        "state_abbrv": "UT",
    },
    {
        "state": "Vermont",
        "latitude": 44.045876,
        "longitude": -72.710686,
        "state_abbrv": "VT",
    },
    {
        "state": "Virginia",
        "latitude": 37.769337,
        "longitude": -78.169968,
        "state_abbrv": "VA",
    },
    {
        "state": "Washington",
        "latitude": 47.400902,
        "longitude": -121.490494,
        "state_abbrv": "WA",
    },
    {
        "state": "West Virginia",
        "latitude": 38.491226,
        "longitude": -80.954453,
        "state_abbrv": "WV",
    },
    {
        "state": "Wisconsin",
        "latitude": 44.268543,
        "longitude": -89.616508,
        "state_abbrv": "WI",
    },
    {
        "state": "Wyoming",
        "latitude": 42.755966,
        "longitude": -107.302490,
        "state_abbrv": "WY",
    },
]

reverse_states_map = {}
for row in states:
    reverse_states_map[row["state_abbrv"]] = row["state"]
# print(reverse_states_map)

states_map = {}
for row in states:
    states_map[row["state"]] = row["state_abbrv"]


class Stats(EmbeddedDocument):
    last_updated = DateTimeField(required=False)
    tested = IntField(required=False)
    confirmed = IntField(required=True)
    deaths = IntField(required=True)


class Country(Document):
    country = StringField(required=True)
    alpha2Code = StringField(max_length=2, required=True)
    lat = FloatField(required=True)
    lon = FloatField(required=True)
    population = IntField(required=False)
    area = IntField(required=False)
    stats = ListField(EmbeddedDocumentField(Stats, required=False))


class State(Document):
    state = StringField(required=True)
    stateAbbr = StringField(max_length=2, required=True)
    lat = FloatField(required=True)
    lon = FloatField(required=True)
    population = IntField(required=False)
    area = IntField(required=False)
    stats = ListField(EmbeddedDocumentField(Stats, required=False))


class County(Document):
    state = StringField(max_length=15, required=True)
    stateAbbr = StringField(max_length=2, required=True)
    county = StringField(max_length=100, require=True)
    fips = IntField(max_length=6, required=True)
    lat = FloatField(required=True)
    lon = FloatField(required=True)
    population = IntField(required=False)
    area = IntField(required=False)
    hospitals = IntField(required=False)
    hospital_beds = IntField(required=False)
    medium_income = IntField(required=False)
    stats = ListField(EmbeddedDocumentField(Stats, required=False))


def ingest_country():
    """ingestion script for country level data"""
    confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

    confirmed = pd.read_csv(confirmed)
    deaths = pd.read_csv(deaths)
    
    print(f"Total Number of Countries confirmed {confirmed['Country/Region'].unique().shape}")
    print(f"Total Number of Countries deaths {deaths['Country/Region'].unique().shape}")

    # fuck princesses
    confirmed = confirmed[confirmed['Country/Region'].isin(country_dict.values())]
    # confirmed = confirmed[confirmed['Country/Region'] != 'Diamond Princess']
    # deaths = deaths[deaths['Country/Region'] != 'Diamond Princess']
    # 'MS Zaandam'
    deaths = deaths[deaths['Country/Region'].isin(country_dict.values())]

    confirmed = confirmed.groupby('Country/Region').sum()
    deaths = deaths.groupby('Country/Region').sum()
    confirmed = confirmed.sort_index().reset_index()
    deaths = deaths.sort_index().reset_index()

    # sanity check
    assert confirmed.shape == deaths.shape
    assert confirmed['Country/Region'][37] == deaths['Country/Region'][37]
    assert confirmed['Country/Region'][115] == deaths['Country/Region'][115]
    assert confirmed['Country/Region'][175] == deaths['Country/Region'][175]
    
    num_countries = confirmed.shape[0]
    dates = confirmed.columns.to_list()[3:]
    
    connect(host=config("MONGODB_CONNECTION_URI"))
    
    for i in range(num_countries):
        # print(confirmed['Country/Region'][i], confirmed['Lat'][i], confirmed['Long'][i])

        stats = []
        for j in range(len(dates)):
            s = Stats(
                last_updated = datetime.strptime(dates[j], "%m/%d/%y"),
                confirmed = confirmed[dates[j]][i],
                deaths = deaths[dates[j]][i],
            )
            stats.append(s)
            
        country = Country(
                    country = confirmed['Country/Region'][i],
                    alpha2Code = reverse_country_map[confirmed['Country/Region'][i]],
                    lat = confirmed['Lat'][i],
                    lon = confirmed['Long'][i],
                    stats = stats,
        )
        
        country.save()
        
    count = 0
    for country in Country.objects:
        print(country.country)
        count += 1

    print(f'Numbers of countries in dataset {num_countries}, ingested {count}')

    disconnect()

    pass


def ingest_county():
    """ingestion script for county level data"""
    confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
    deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

    confirmed = pd.read_csv(confirmed)
    deaths = pd.read_csv(deaths)

    confirmed = confirmed[confirmed['Province_State'].isin(reverse_states_map.values())]
    deaths = deaths[deaths['Province_State'].isin(reverse_states_map.values())]

    print(f"Total Number of counties confirmed {confirmed['Admin2'].unique().shape}")
    print(f"Total Number of counties deaths {deaths['Admin2'].unique().shape}")

    # Admin2,Province_State,Country_Region
    dates = confirmed.columns.to_list()[11:]

    assert confirmed['Admin2'][37] == deaths['Admin2'][37]
    assert confirmed['Admin2'][1115] == deaths['Admin2'][1115]
    assert confirmed['Admin2'][1715] == deaths['Admin2'][1715]
    
    num_counties = confirmed.shape[0]
    # dates = confirmed.columns.to_list()[3:]

    connect(host=config("MONGODB_CONNECTION_URI"))

    # have to use iloc otherwise code breaks by straight indexing.
    for i in range(num_counties):

        stats = []
        for j in range(len(dates)):
            s = Stats(
                last_updated = datetime.strptime(dates[j], "%m/%d/%Y"),
                confirmed = confirmed[dates[j]].iloc[i],
                deaths = deaths[dates[j]].iloc[i],
            )
            stats.append(s)
            
        county = County(
                    state = confirmed['Province_State'].iloc[i],
                    stateAbbr = states_map[confirmed['Province_State'].iloc[i]],
                    county = confirmed['Admin2'].iloc[i],
                    fips = confirmed['FIPS'].iloc[i],
                    lat = confirmed['Lat'].iloc[i],
                    lon = confirmed['Long_'].iloc[i],
                    population = deaths['Population'].iloc[i],
                    area = 0,
                    hospitals = 0,
                    hospital_beds = 0,
                    medium_income = 0,
                    stats = stats,
        )
        
        county.save()
        
    count = 0
    for county in County.objects:
        print(county.county)
        count += 1

    print(f'Numbers of countries in dataset {num_counties}, ingested {count}')

    disconnect()

    pass


def main():
    # ingest_country()
    ingest_county()


if __name__ == "__main__":
    main()
