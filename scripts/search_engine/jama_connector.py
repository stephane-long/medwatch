import html
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import List

import httpx
from models import Article


def fetch_from_jama(query: str = "", days: int = 1) -> List[Article]:
    """
    Récupère les articles depuis les flux RSS de JAMA.
    """
    urls = [
        "https://jamanetwork.com/rss/site_3/onlineFirst_67.xml",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    articles = []
    query_lower = query.lower() if query else ""

    with httpx.Client(follow_redirects=True) as client:
        for url in urls:
            try:
                response = client.get(url, headers=headers)
                response.raise_for_status()

                content = response.content.strip()
                root = ET.fromstring(content)
                items = root.findall(".//item")

                for item in items:
                    title = item.findtext("title", "")
                    link = item.findtext("link", "")
                    # JAMA format: Mon, 09 Mar 2026 00:00:00 GMT
                    pub_date_raw = item.findtext("pubDate", "")
                    description = item.findtext("description", "")

                    # Filtrage par mots-clés
                    if (
                        query_lower
                        and query_lower != "jama"
                        and query_lower not in title.lower()
                        and query_lower not in description.lower()
                    ):
                        continue

                    # Conversion de la date
                    dt = None
                    date_publication = pub_date_raw
                    try:
                        # Format: Mon, 09 Mar 2026 00:00:00 GMT
                        # %Z peut être capricieux avec GMT selon la plateforme, on peut utiliser %z si on remplace GMT par +0000
                        # ou simplement parser tel quel si l'OS le supporte.
                        clean_date = pub_date_raw.replace("GMT", "+0000")
                        dt = datetime.strptime(clean_date, "%a, %d %b %Y %H:%M:%S %z")
                        date_publication = dt.strftime("%Y-%m-%d")
                    except Exception:
                        try:
                            # Fallback sans timezone si le premier échoue
                            dt = datetime.strptime(pub_date_raw, "%a, %d %b %Y %H:%M:%S %Z")
                            date_publication = dt.strftime("%Y-%m-%d")
                        except Exception:
                            pass

                    # Filtrage par date si days > 0 et date parsée — sinon on conserve l'article
                    if days > 0 and dt:
                        now = datetime.now(dt.tzinfo)
                        cutoff = (now - timedelta(days=days)).replace(hour=0, minute=0, second=0, microsecond=0)
                        if dt < cutoff:
                            continue

                    # Nettoyage HTML
                    extrait_clean = re.sub(r"<[^>]+>", "", description).strip()
                    extrait = html.unescape(extrait_clean)
                    title = html.unescape(title)

                    article = Article(
                        titre=title,
                        url=link,
                        date_publication=date_publication,
                        source="JAMA",
                        moteur="JAMA",
                        extrait=extrait or title,
                    )
                    articles.append(article)

            except Exception as e:
                print(f"Erreur lors de la récupération JAMA ({url}): {e}", file=sys.stderr)

    return articles
