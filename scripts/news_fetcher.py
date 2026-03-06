import requests
import os
import sys
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Remplacez par votre clé NewsAPI
NEWSAPI_API_KEY = os.getenv("NEWSAPI_API_KEY")


def search_news(query, days=1):
    # Calcul de la date de début
    from_date = (datetime.now() - timedelta(days=int(days))).strftime("%Y-%m-%d")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": from_date,
        "sortBy": "relevancy",
        "language": "fr",
        "apiKey": NEWSAPI_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("articles", [])
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Query missing"}))
        sys.exit(1)

    user_query = sys.argv[1]
    days_to_search = sys.argv[2] if len(sys.argv) > 2 else 1

    results = search_news(user_query, days_to_search)
    print(json.dumps(results, indent=2))
