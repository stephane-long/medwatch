# Expose de manière propre les fonctions des connecteurs
from .newsapi_connector import fetch_from_newsapi
from .tavily_connector import fetch_from_tavily
from .google_news_connector import fetch_from_googlenews
from .ansm_connector import fetch_from_ansm

__all__ = ["fetch_from_newsapi", "fetch_from_tavily", "fetch_from_googlenews", "fetch_from_ansm"]
