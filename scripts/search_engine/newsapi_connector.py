import os
import sys
from datetime import datetime, timedelta
from typing import List

from models import Article
from newsapi import NewsApiClient


def fetch_from_newsapi(query: str, days: int = 1) -> List[Article]:
    """
    Interroge NewsAPI et renvoie une liste standardisée d'objets Article.
    """
    api_key = os.getenv("NEWSAPI_API_KEY")
    if not api_key:
        print("Avertissement: NEWSAPI_API_KEY non définie.", file=sys.stderr)
        return []

    # Calcul de la date de début
    from_date = (datetime.now() - timedelta(days=int(days))).strftime("%Y-%m-%d")
    newsapi = NewsApiClient(api_key=api_key)

    articles_trouves: List[Article] = []

    try:
        response = newsapi.get_everything(
            q=query, from_param=from_date, language="fr", sort_by="relevancy"
        )

        if response.get("status") == "ok":
            for item in response.get("articles", []):
                # On ignore les articles sans URL ou sans titre
                if (
                    not item.get("url")
                    or not item.get("title")
                    or item.get("title") == "[Removed]"
                ):
                    continue

                # Gestion de la date de publication
                published_at = item.get("publishedAt", "")
                if "T" in published_at:
                    published_at = published_at.split("T")[
                        0
                    ]  # On garde juste YYYY-MM-DD
                if not published_at:
                    published_at = datetime.now().strftime("%Y-%m-%d")

                try:
                    article = Article(
                        titre=item.get("title", ""),
                        url=item.get("url", ""),
                        date_publication=published_at,
                        source=item.get("source", {}).get("name", "NewsAPI"),
                        moteur="NewsAPI",
                        extrait=item.get("description")
                        or item.get("content")
                        or "Aucun extrait disponible.",
                        score=None,
                    )
                    articles_trouves.append(article)
                except Exception:
                    # Si Pydantic rejette un article (titre vide, etc.), on l'ignore silencieusement
                    pass

    except Exception as e:
        print(f"Erreur lors de la requête NewsAPI: {str(e)}", file=sys.stderr)

    return articles_trouves
