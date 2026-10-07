import concurrent.futures
import sys
from typing import List

from models import Article, ReponseGlobale
from processing import process_results
from search_engine import (
    fetch_from_ansm,
    fetch_from_googlenews,
    fetch_from_newsapi,
    fetch_from_tavily,
    fetch_from_jama,
)


def run_pipeline(query: str, days: int = 1, profile: str = "sociopro") -> ReponseGlobale:
    """
    Orchestre les requêtes en parallèle vers les moteurs de recherche
    sélectionnés selon le profil, puis traite et renvoie les résultats combinés.

    Profils :
    - sociopro : NewsAPI, Tavily, Google News, ANSM
    - medical  : JAMA, ANSM
    """
    all_articles: List[Article] = []

    # Définition des connecteurs par profil
    futures = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Connecteurs communs ou spécifiques selon le profil
        if profile == "sociopro":
            futures["NewsAPI"] = executor.submit(fetch_from_newsapi, query, days)
            futures["Tavily"] = executor.submit(fetch_from_tavily, query, days)
            futures["GoogleNews"] = executor.submit(fetch_from_googlenews, query, days)
            futures["ANSM"] = executor.submit(fetch_from_ansm, query, days)
        elif profile == "medical":
            futures["JAMA"] = executor.submit(fetch_from_jama, days)
            futures["ANSM"] = executor.submit(fetch_from_ansm, query, days)

        # Récupération des résultats
        for name, future in futures.items():
            try:
                all_articles.extend(future.result())
            except Exception as e:
                print(f"La pipeline a intercepté une erreur {name}: {e}", file=sys.stderr)

    # Passage au processeur pour déduplication et construction de la réponse
    final_response = process_results(query, all_articles)
    # final_response = all_articles

    return final_response
