# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Présentation

MedWatch est un **skill agentique de veille médicale** destiné aux journalistes. Il combine un ensemble de scripts Python (collecte multi-sources) avec des instructions LLM (`SKILL.md`) pour produire des revues de presse structurées au format Markdown.

Le skill est invocable via la commande `/medwatch` dans Claude Code.

## Commandes

### Installation
```bash
python -m venv scripts/.venv
pip install -r scripts/requirements.txt
```

### Exécution
```bash
# macOS/Linux
scripts/.venv/bin/python -X utf8 scripts/news_fetcher.py "requête" --days 1

# Windows
scripts/.venv/Scripts/python.exe -X utf8 scripts/news_fetcher.py "requête" --days 1
```

Le flag `-X utf8` est obligatoire pour éviter les problèmes d'encodage (notamment sur Windows).

### Configuration
Créer `scripts/.env` avec :
```
NEWSAPI_KEY=votre_cle
TAVILY_API_KEY=votre_cle
```

Il n'y a pas de tests automatisés dans ce projet.

## Architecture

```
medwatch/
├── SKILL.md              # Instructions LLM du skill (invocable via /medwatch)
├── TEMPLATE.md           # Template Markdown du rapport de sortie (référencé par SKILL.md)
├── reports/              # Rapports générés (un fichier .md par veille)
└── scripts/
    ├── news_fetcher.py       # Point d'entrée CLI (Typer), émet du JSON vers stdout
    ├── pipeline.py           # Orchestrateur : lance 5 connecteurs en parallèle (ThreadPoolExecutor, 5 workers)
    ├── models.py             # Modèles Pydantic : Article, ReponseGlobale
    ├── processing.py         # Déduplication par URL, limitation à 100 articles
    └── search_engine/
        ├── newsapi_connector.py      # API NewsAPI (langue fr, tri par pertinence)
        ├── tavily_connector.py       # API Tavily (search depth avancée, topic news)
        ├── google_news_connector.py  # RSS Google News (parsing XML, hl=fr&gl=FR)
        ├── ansm_connector.py         # 3 flux RSS ANSM filtrés par mots-clés
        └── jama_connector.py         # RSS JAMA online-first publications
```

### Flux de données

1. `news_fetcher.py` reçoit `(query, days)` via CLI
2. `pipeline.py` soumet les 5 connecteurs en parallèle ; chaque échec individuel est capturé silencieusement (résultats partiels)
3. `processing.py` déduplique par URL puis limite à 100 articles
4. Le résultat est sérialisé en JSON minifié vers stdout (pour consommation LLM)

### Contrat des connecteurs

La plupart suivent `fetch_from_X(query: str, days: int) -> List[Article]`. Exception : **JAMA** n'accepte que `days` (pas de `query`), car il retourne toujours les dernières publications online-first sans filtrage par mots-clés.

Le modèle `Article` (Pydantic v2) valide : `titre`, `url` (HttpUrl), `date_publication`, `source`, `moteur`, `extrait`, `score`. Un validateur préfixe automatiquement `extrait` avec le nom de la source pour faciliter la recherche par mots-clés.

### Output LLM

La réponse finale (`ReponseGlobale`) est un objet JSON avec : `requete`, `statut`, `nombre_articles_trouves`, `nombre_articles_par_source`, `articles`, `message_erreur`.

Les rapports sont enregistrés dans `reports/{query_sanitisée}_{date}.md` selon le format défini dans `TEMPLATE.md`.

### Prétraitement des requêtes (règle clé du skill)

Avant d'exécuter la commande, toute requête brute doit être enrichie avec des termes connexes via `OR`. Exemples :
- `"médecins"` → `"médecins OR santé OR hôpital OR système de soins"`
- `"ANSM"` → `"ANSM OR alerte médicament OR sécurité sanitaire"`
- `"diabète"` → `"diabète OR hyperglycémie OR traitement du diabète OR insuline"`

Les requêtes très spécifiques (ex. "maladie de Crohn") peuvent rester telles quelles ou avec un enrichissement léger. Voir `SKILL.md` pour la table complète des heuristiques.
