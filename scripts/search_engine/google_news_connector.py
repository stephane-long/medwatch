import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List
import re
import html
from models import Article

def fetch_from_googlenews(query: str, days: int = 1) -> List[Article]:
    """
    Récupère les articles depuis le flux RSS de Google News.
    """
    url = f"https://news.google.com/rss/search?q={query}&hl=fr&gl=FR&ceid=FR%3Af"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    articles = []
    try:
        with httpx.Client(follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            items = root.findall(".//item")
            
            for item in items:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date_raw = item.findtext("pubDate", "")
                description = item.findtext("description", "")
                source_elem = item.find("source")
                source_name = source_elem.text if source_elem is not None else "Google News"
                
                # Conversion de la date (format RSS: Mon, 09 Mar 2026 17:00:02 GMT)
                try:
                    dt = datetime.strptime(pub_date_raw, "%a, %d %b %Y %H:%M:%S %Z")
                    date_publication = dt.strftime("%Y-%m-%d")
                except Exception:
                    date_publication = pub_date_raw
                
                # Nettoyage HTML et décodage des entités (ex: &nbsp;)
                extrait_clean = re.sub(r"<[^>]+>", "", description).strip()
                extrait = html.unescape(extrait_clean)
                title = html.unescape(title)
                
                article = Article(
                    titre=title,
                    url=link,
                    date_publication=date_publication,
                    source=source_name,
                    moteur="GoogleNews",
                    extrait=extrait or title,
                )
                articles.append(article)
                
    except Exception as e:
        print(f"Erreur lors de la récupération Google News: {e}")
        
    return articles
