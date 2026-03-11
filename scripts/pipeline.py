import concurrent.futures
from typing import List

from models import Article, ReponseGlobale
from processing import process_results
from search_engine import (
    fetch_from_googlenews,
    fetch_from_newsapi,
    fetch_from_tavily,
    fetch_from_ansm,
)


def run_pipeline(query: str, days: int = 1) -> ReponseGlobale:
    """
    Orchestre les requêtes en parallèle vers les différents moteurs de recherche,
    puis traite et renvoie les résultats combinés.
    """
    all_articles: List[Article] = []

    # Exécution des appels API en parallèle grâce à ThreadPoolExecutor
    # Plus on ajoute de connecteurs, plus c'est efficace par rapport à l'approche séquentielle.
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # On soumet les tâches
        future_newsapi = executor.submit(fetch_from_newsapi, query, days)
        future_tavily = executor.submit(fetch_from_tavily, query, days)
        future_googlenews = executor.submit(fetch_from_googlenews, query, days)
        future_ansm = executor.submit(fetch_from_ansm, query, days)

        # On récupère les résultats dès qu'ils sont prêts
        try:
            articles_newsapi = future_newsapi.result()
            all_articles.extend(articles_newsapi)
        except Exception as e:
            print(f"La pipeline a intercepté une erreur NewsAPI: {e}")

        try:
            articles_tavily = future_tavily.result()
            all_articles.extend(articles_tavily)
        except Exception as e:
            print(f"La pipeline a intercepté une erreur Tavily: {e}")

        try:
            articles_googlenews = future_googlenews.result()
            all_articles.extend(articles_googlenews)
        except Exception as e:
            print(f"La pipeline a intercepté une erreur GoogleNews: {e}")

        try:
            articles_ansm = future_ansm.result()
            all_articles.extend(articles_ansm)
        except Exception as e:
            print(f"La pipeline a intercepté une erreur ANSM: {e}")

    # Passage au processeur pour déduplication et construction de la réponse
    final_response = process_results(query, all_articles)
    # final_response = all_articles

    return final_response
