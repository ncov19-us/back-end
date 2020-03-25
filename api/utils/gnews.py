import pandas as pd
from bs4 import BeautifulSoup
import requests
from api.config import Config


def get_state_topic_google_news(state, topic, max_rows=10):
    """This function takes a US State name (string dtype) and a topic of interest (string dtype). 
    The output is a pandas DataFrame with articles, urls, and publishing times for articles containing the state and topic
    """

    url = "https://news.google.com/rss/search?q={}+{}&hl=en-US&gl=US&ceid=US:en".format(
        state, topic
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
    df.iloc[: min(len(df), max_rows)]
    return convert_df_to_json(df)


def convert_df_to_json(df):
    data = pd.DataFrame.to_json(df, orient="records")
    return data


def get_us_news(max_rows=50):
    news_requests = requests.get(Config.NEWS_API_URL)
    json_data = news_requests.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title", "url", "publishedAt"]])
    # Infer datetime
    df["publishedAt"] = pd.to_datetime(df["publishedAt"], infer_datetime_format=True)
    # Assuming timedelta of 5 hours based on what i compared from CNN articles from API.
    df["publishedAt"] = df["publishedAt"] - pd.Timedelta("5 hours")
    """
    # Format date time way you want to display, https://strftime.org/
    """

    def dt_fmt(val):
        return val.strftime("%a %d, %Y, %I: %M %p ET")

    # Apply pandas function to format news published date
    df["publishedAt"] = df["publishedAt"].apply(dt_fmt)
    df = df.iloc[: min(len(df), max_rows)]
    return convert_df_to_json(df)


if __name__ == "__main__":
    pass
