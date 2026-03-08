from typing import List

from models import Article, ReponseGlobale


def deduplicate_articles(articles: List[Article]) -> List[Article]:
    """
    Supprime les doublons en se basant sur l'URL de l'article.
    """
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url_str = str(article.url)
        if url_str not in seen_urls:
            unique_articles.append(article)
            seen_urls.add(url_str)

    return unique_articles


def limit_results(articles: List[Article], max_items: int = 15) -> List[Article]:
    """
    Limite le nombre d'articles pour ne pas saturer la fenêtre de contexte de Claude.
    """
    return articles[:max_items]


def process_results(query: str, raw_articles: List[Article]) -> ReponseGlobale:
    """
    Traite la liste brute d'articles, enlève les doublons et renvoie
    l'objet de réponse finale formaté pour l'IA.
    """
    unique_articles = deduplicate_articles(raw_articles)
    final_articles = limit_results(unique_articles, 50)

    comptage_sources = {}
    for article in final_articles:
        moteur = article.moteur
        comptage_sources[moteur] = comptage_sources.get(moteur, 0) + 1

    return ReponseGlobale(
        requete=query,
        statut="succès",
        nombre_articles_trouves=len(final_articles),
        nombre_articles_par_source=comptage_sources,
        articles=final_articles,
    )
