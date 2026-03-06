import os
import sys
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from newsapi import NewsApiClient


load_dotenv()
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")


def deduplicate_sources(sources):
    seen_url = set()
    unique = []

    for source in sources:
        url = source.get("url", "")
        if url and url not in seen_url:
            unique.append(url)
            seen_url.add(url)
    return unique


def search_newsapi(query, days=1):
    # Calcul de la date de début
    from_date = (datetime.now() - timedelta(days=int(days))).strftime("%Y-%m-%d")

    newsapi = NewsApiClient(api_key=NEWSAPI_API_KEY)

    try:
        all_articles = newsapi.get_everything(
            q=query, from_param=from_date, language="fr", sort_by="relevancy"
        )
        return all_articles
    except Exception as e:
        return {"error": str(e)}


def search_tavily(query, days):
    pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Query missing"}))
        sys.exit(1)

    user_query = sys.argv[1]
    days_to_search = sys.argv[2] if len(sys.argv) > 2 else 1

    results = search_newsapi(user_query, days_to_search)

    sources = deduplicate_sources(results.get("articles", ""))
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"Doublons : {int(results.get('totalResults')) - len(sources)}")
