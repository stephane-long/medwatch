# MedWatch - Skill de Veille Médicale

MedWatch est un skill agentique permettant d'effectuer une veille sur l'actualité médicale. Il associe des outils de récupération de données à un ensemble de directives pour l'analyse et la structuration des informations par un assistant IA.

## Architecture du Skill

Le projet est composé de deux parties :

1.  **Instructions du Skill (`SKILL.md`)** : Regroupe les règles d'analyse, les critères de sélection des articles (pertinence, exhaustivité, sources de référence) et le format des rapports attendus.
2.  **Outils d'exécution (`scripts/`)** : Ensemble de scripts Python permettant d'interroger plusieurs sources de données (NewsAPI, Tavily, Google News RSS) et de normaliser les résultats.

## Fonctionnalités

- **Agrégation multi-sources** : Récupération d'articles depuis différentes API et flux RSS.
- **Traitement parallèle** : Utilisation d'une pipeline multithreadée pour optimiser les temps de réponse.
- **Sélection et analyse** : Filtrage des articles selon des axes thématiques (Clinique, Institutionnel, Socio-professionnel, Innovation).
- **Formatage des résultats** : Génération automatique de rapports structurés au format Markdown.

## Composants Techniques

- `scripts/news_fetcher.py` : Interface en ligne de commande pour lancer la collecte.
- `scripts/pipeline.py` : Orchestrateur gérant l'exécution des connecteurs.
- `scripts/search_engine/google_news_connector.py` : Connecteur pour les flux RSS de Google News.
- `scripts/models.py` : Modèles de données Pydantic pour la validation et l'échange d'informations.

## Installation et Utilisation

### Installation
```bash
python -m venv scripts/.venv
pip install -r scripts/requirements.txt
```

### Configuration
Le fichier `scripts/.env` doit contenir les clés d'accès nécessaires :
```env
NEWSAPI_KEY=votre_cle
TAVILY_API_KEY=votre_cle
```

### Utilisation via l'IA
Le skill est activé par l'assistant IA en exécutant la commande suivante :
```bash
python scripts/news_fetcher.py "mots_clés" --days 1
```
