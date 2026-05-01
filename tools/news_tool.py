from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_news(query: str)-> str:
    " takes a topic and returns latest news article about it"

    try:
        client = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))

        response = client.get_top_headlines(
            q = query,
            language = "en",
            page_size = 5
        )

        articles = []

        for article in response["articles"]:
            articles.append(
                f'Headline: {article["title"]}\n'
                f'Source: {article["source"]["name"]}\n'
                f'Published: {article["PubhlishedAt"]}\n'
                f'Summary:{article["description"]}\n'

            )

        return "\n".join(articles)
        
    except Exception as e:
        return f'News fetch failed: {str(e)}'