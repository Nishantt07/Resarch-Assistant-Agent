from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

def web_search(query: str) -> str:
    " Takes a search query and returns top results from the web"

    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        response = client.search(
            query= query,
            search_depth="advanced",
            max_results=5
        )



        results = []

        for item in response["results"]:
            print(item["title"])
            print(item["url"])
            results.append(f"Title:{ item['title']} \n URL:{item['url']} \n Summary: {item['content']} \n")

        return "\n".join(results)
        
    except Exception as e:
        return f'Web Search failed: {str(e)}'
        
