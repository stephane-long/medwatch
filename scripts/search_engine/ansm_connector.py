import html
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List

import httpx
from models import Article


def fetch_from_ansm(query: str = "", days: int = 1) -> List[Article]:
    """
    Récupère les articles depuis les flux RSS de l'ANSM.
    """
    urls = [
        "https://ansm.sante.fr/rss/informations_securite",
        "https://ansm.sante.fr/rss/actualites",
        "https://ansm.sante.fr/rss/disponibilite_produits_sante",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    articles = []

    # On normalise la requête pour le filtrage
    query_lower = query.lower() if query else ""

    with httpx.Client(follow_redirects=True) as client:
        for url in urls:
            try:
                response = client.get(url, headers=headers)
                response.raise_for_status()

                # Correction potentielle si le XML est mal formé avec des espaces au début
                content = response.content.strip()
                root = ET.fromstring(content)
                items = root.findall(".//item")

                for item in items:
                    title = item.findtext("title", "")
                    link = item.findtext("link", "")
                    pub_date_raw = item.findtext("pubDate", "")
                    description = item.findtext("description", "")

                    # Filtrage par mots-clés si une requête est fournie
                    # Si la requête est "ANSM", on considère que tout est pertinent car c'est la source même
                    if (
                        query_lower
                        and query_lower != "ansm"
                        and query_lower not in title.lower()
                        and query_lower not in description.lower()
                    ):
                        continue

                    # Conversion de la date (format attendu: Wed, 11 Mar 2026 14:00:00 +0100)
                    dt = None
                    date_publication = pub_date_raw
                    try:
                        dt = datetime.strptime(pub_date_raw, "%a, %d %b %Y %H:%M:%S %z")
                        date_publication = dt.strftime("%Y-%m-%d")
                    except Exception:
                        pass

                    # Nettoyage HTML basique
                    extrait_clean = re.sub(r"<[^>]+>", "", description).strip()
                    extrait = html.unescape(extrait_clean)
                    title = html.unescape(title)

                    # Filtrage par date si days > 0 et date parsée — sinon on conserve l'article
                    if days > 0 and dt:
                        now = datetime.now(dt.tzinfo)
                        cutoff = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
                        if dt < cutoff:
                            continue

                    article = Article(
                        titre=title,
                        url=link,
                        date_publication=date_publication,
                        source="ANSM",
                        moteur="ANSM",
                        extrait=extrait or title,
                    )
                    articles.append(article)

            except Exception as e:
                print(f"Erreur lors de la récupération ANSM ({url}): {e}", file=sys.stderr)

    return articles
