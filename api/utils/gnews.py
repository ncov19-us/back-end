import gc
from typing import Dict

import requests
import pandas as pd

from bs4 import BeautifulSoup
from api.config import app_config


def get_state_topic_google_news(state: str, topic: str, max_rows: int = 10) -> Dict:
    """This function takes a US State name (string dtype) and a topic of
    interest (string dtype). The output is a pandas DataFrame with articles,
    urls, and publishing times for articles containing the state and topic

    :param: :state: :str: state, the state to query Google News API
    :param: :topic: :str: topic, the topic to query Google News API
    :param: :max_rows: :int: number of rows to return

    :return: :Dict: python dictionary of the data for pydantic to force
                    type checking.
    """

    url = (
        "https://news.google.com/rss/search?"
        f"q={state}+{topic}&hl=en-US&gl=US&ceid=US:en"
    )
    list_of_titles = []
    list_of_article_links = []
    list_of_pubdates = []
    state_id_for_articles = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    xml = str(list(soup)).split("<item><title>")

    for i in range(len(xml[1:])):
        list_of_titles.append(xml[i + 1].split("</title>")[0])
        list_of_article_links.append(
            xml[i + 1].split("</title><link/>")[1].split("<guid ispermalink")[0]
        )
        list_of_pubdates.append(
            xml[i + 1].split("</guid><pubdate>")[1].split("</pubdate>")[0]
        )
        state_id_for_articles.append(state)

    df = pd.DataFrame(
        [list_of_titles, list_of_article_links, list_of_pubdates, state_id_for_articles]
    ).T
    df.columns = ["title", "url", "published", "state"]
    df["source"] = df["title"].str.split("-").str[-1]
    df = df.iloc[: min(len(df), max_rows)]

    result = df.to_dict(orient="records")

    del df, page, soup, xml
    gc.collect()

    return result


def get_us_news(max_rows: int = 50) -> Dict:
    """This function gathers news from the whole US from the past 5 hours.

    :param: :max_rows: :int: number of rows to return
    :return: :Dict: python dictionary of the data for type checking.
    """

    news_requests = requests.get(app_config.NEWS_API_URL)
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url", "publishedAt"]])
    df = df.rename(columns={"publishedAt": "published"})
    # Infer datetime
    df["published"] = pd.to_datetime(df["published"], infer_datetime_format=True)
    # Assuming timedelta of 5 hr based on what comparison between CNN and API.
    df["published"] = df["published"] - pd.Timedelta("5 hours")

    def dt_fmt(val):
        """Format date time way you want to display, https://strftime.org/"""
        return val.strftime("%a %d, %Y, %I: %M %p ET")

    # Apply pandas function to format news published date
    df["published"] = df["published"].apply(dt_fmt)
    df = df.iloc[: min(len(df), max_rows)]

    result = df.to_dict(orient="records")

    del news_requests, json_data, df
    gc.collect()

    return result


if __name__ == "__main__":
    pass
