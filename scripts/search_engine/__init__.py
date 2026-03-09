# Expose de manière propre les fonctions des connecteurs
from .newsapi_connector import fetch_from_newsapi
from .tavily_connector import fetch_from_tavily
from .google_news_connector import fetch_from_googlenews

__all__ = ["fetch_from_newsapi", "fetch_from_tavily", "fetch_from_googlenews"]
