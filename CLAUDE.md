# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Medwatch** is an AI-powered medical news surveillance tool designed for journalists to monitor healthcare, medical research, and professional health topics.

The project integrates NewsAPI and Tavily as search sources, with structured markdown reports as output.

## Quick Start

### Setup
1. **Créer le venv** : `python3 -m venv scripts/.venv`
2. **Installer les dépendances** : `pip install -r scripts/requirements.txt`
3. **Configurer les clés API** : créer un fichier `.env` à la racine avec :
   ```
   NEWSAPI_API_KEY=votre_cle_newsapi
   TAVILY_API_KEY=votre_cle_tavily
   ```
4. **Lancer une recherche** : `scripts/.venv/bin/python3 scripts/news_fetcher.py "query text" [days]`
   - Exemple : `scripts/.venv/bin/python3 scripts/news_fetcher.py "maladie de Crohn" 7`
   - Retourne un JSON des résultats Tavily

### As a Claude Skill
Le skill est défini dans SKILL.md. Claude :
1. Extrait la requête et la période depuis l'intention de l'utilisateur
2. Exécute le script via le venv
3. Formate les résultats et les écrit dans `reports/`

## Architecture

### Structure actuelle
```
medwatch/
├── CLAUDE.md              # Ce fichier
├── SKILL.md               # Configuration du Claude Skill
├── reports/               # Rapports générés en markdown
│   └── {query}_{date}.md
└── scripts/
    ├── news_fetcher.py    # Point d'entrée principal
    ├── requirements.txt   # Dépendances figées
    └── .venv/             # Environnement virtuel Python
```

### Fonctionnement actuel
- **Source active** : Tavily API (recherche web avancée avec filtre de dates)
- **Source disponible** : NewsAPI (intégrée mais commentée dans `__main__`)
- **Déduplication** : fonction `deduplicate_sources()` disponible (non active sur Tavily)
- **Output** : JSON brut retourné par le script, mis en forme par SKILL.md → fichiers `reports/`

### Architecture cible (Phase 2)
- **Sources supplémentaires** : PubMed RSS + scraping Tier 1 (HAS, Ansm, Santé Publique France)
- **Classification des sources** : Tier 1=Autorités, 2=Académique, 3=Médias, 4=Autre
- **Extraction de contenu** : résumés 300-500 caractères depuis les articles complets
- **Orchestrateur** : `orchestrator.py` → search → extract → synthesize → report

## Key Implementation Notes

### SKILL.md Contract
- Commande : `scripts/.venv/bin/python3 scripts/news_fetcher.py "{query}" {days}`
- Output attendu : JSON (objet Tavily ou objet erreur)
- Responsabilité de Claude : prétraitement de la requête, filtrage pertinence, rédaction résumés, écriture dans `reports/`

**Important** : conserver un output JSON valide pour que Claude puisse parser les résultats.

### Gestion des clés API
- Les deux clés doivent être dans `.env` à la racine (chargé via `python-dotenv`)
- NewsAPI : free tier 100 req/jour — suffisant pour dev/test
- Tavily : vérifier les quotas selon le plan souscrit

### Known Issues
- NewsAPI désactivé dans `__main__` (commenté) — les lignes `deduplicate_sources` associées sont aussi commentées.

## Development Practices

- **Language** : Python 3.9+
- **Dependencies** : gérées via `scripts/requirements.txt` + venv dans `scripts/.venv/`
- **Testing** : tests unitaires dans `tests/` (pytest)
- **Code style** : PEP 8
- **API keys** : jamais commitées — utiliser `.env` (ignoré par git)

## Reference Documents

- **SKILL.md** : configuration du skill, format de commande, format de sortie attendu
- **newsapi.org** : documentation API et inscription free tier
- **tavily.com** : documentation API Tavily
