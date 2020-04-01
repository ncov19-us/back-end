from datetime import datetime
from decouple import config
import pandas as pd
from mongoengine import *

# from api.config import MONGODB_CONNECTION_URI
import pymongo
import pprint


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
                    alpha2Code = 'NA',
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
    info = confirmed.columns[:10]
    print(info)
    
    print(f"Total Number of counties confirmed {confirmed['Country/Region'].unique().shape}")
    print(f"Total Number of counties deaths {deaths['Country/Region'].unique().shape}")

    # confirmed = confirmed.groupby('Country/Region').sum()
    # deaths = deaths.groupby('Country/Region').sum()
    # confirmed = confirmed.sort_index().reset_index()
    # deaths = deaths.sort_index().reset_index()

    dates = confirmed.columns[11:]
    print(dates)

    # for county in County.objects:
    #     print(county.state)
    
    # county = County(state="Michigan",
    #                 stateAbbr="MI",
    #                 county="Deer Field",
    #                 fips=12345,
    #                 lat=12.34567,
    #                 lon=89.01234,
    #                 stats=Stats(
    #                     last_updated="2020-03-31",
    #                     confirmed=12345,
    #                     deaths=67890,
    #                     )
    #                 )
    # county.save()


    # # tm = TestMongo(db_name="covid-staging", collection_name="county")
    # print(tm.collection.find())
    pass


def main():
    ingest_county()


if __name__ == "__main__":
    main()
