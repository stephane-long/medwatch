# Expose de manière propre les fonctions des connecteurs
from .newsapi_connector import fetch_from_newsapi
from .tavily_connector import fetch_from_tavily

__all__ = ["fetch_from_newsapi", "fetch_from_tavily"]
