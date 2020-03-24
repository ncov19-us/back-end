import pandas as pd


def get_state_topic_google_news(state, topic):
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

    for i in range(len(xml[1:-1])):
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
    return df


def convert_df_to_json(df):
    return pd.DataFrame.to_json(df, orient="records")
