import os
from datetime import datetime
from typing import List

from models import Article
from tavily import TavilyClient


def fetch_from_tavily(query: str, days: int = 1) -> List[Article]:
    """
    Interroge Tavily Search et renvoie une liste standardisée d'objets Article.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("Avertissement: TAVILY_API_KEY non définie.")
        return []

    client = TavilyClient(api_key=api_key)
    articles_trouves: List[Article] = []

    try:
        # On demande une recherche ciblée sur l'actualité si possible,
        # topic="news" est supporté par Tavily pour privilégier les articles récents
        response = client.search(
            query=query,
            search_depth="advanced",
            topic="news",
            days=days,
            include_images=False,
        )

        for item in response.get("results", []):
            if not item.get("url") or not item.get("title"):
                continue

            # Tavily renvoie parfois une date dans 'published_date' s'il s'agit de news
            published_at = item.get("published_date", "")
            if "T" in published_at:
                published_at = published_at.split("T")[0]
            elif " " in published_at:
                published_at = published_at.split(" ")[0]
            if not published_at:
                published_at = datetime.now().strftime("%Y-%m-%d")

            try:
                raw_content = item.get("content") or "Aucun extrait disponible."
                article = Article(
                    titre=item.get("title", ""),
                    url=item.get("url", ""),
                    date_publication=published_at,
                    source=item.get("url", "").split("/")[2]
                    if "://" in str(item.get("url", ""))
                    else "Tavily",  # Extraction basique du domaine
                    moteur="Tavily",
                    extrait=raw_content[:2000],
                    score=item.get("score"),
                )
                articles_trouves.append(article)
            except Exception as e:
                print(f"Validation error for {item.get('title')}: {e}")

    except Exception as e:
        print(f"Erreur lors de la requête Tavily: {str(e)}")

    return articles_trouves
