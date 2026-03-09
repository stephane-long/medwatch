# MedWatch - Veille d'actualité médicale

MedWatch est un outil de veille automatisé conçu pour agréger et analyser des actualités médicales provenant de sources multiples. Il permet de générer des rapports structurés pour aider les professionnels de santé à rester informés des dernières évolutions de leur secteur.

## Fonctionnalités

- **Agrégation multi-sources** : Récupère des articles via NewsAPI, Tavily et Google News RSS.
- **Traitement en parallèle** : Utilise `ThreadPoolExecutor` pour des performances optimales lors de la récupération des données.
- **Normalisation des données** : Formate les résultats selon un modèle Pydantic strict pour une analyse facilitée par IA.
- **Génération de rapports** : Produit des synthèses structurées en Markdown dans le dossier `reports/`.

## Structure du projet

- `scripts/` : Contient le cœur logique de l'application.
  - `news_fetcher.py` : Point d'entrée CLI (Typer) pour lancer les recherches.
  - `pipeline.py` : Orchestrateur gérant les appels parallèles aux connecteurs.
  - `search_engine/` : Connecteurs spécifiques pour chaque source d'actualités.
  - `models.py` : Définitions des modèles de données (Pydantic).
- `reports/` : Dossier de destination des rapports de veille générés.
- `SKILL.md` : Instructions détaillées pour l'assistant IA sur la manière de mener les veilles.

## Installation

1. Créer un environnement virtuel :
   ```bash
   python -m venv scripts/.venv
   ```
2. Installer les dépendances :
   ```bash
   pip install -r scripts/requirements.txt
   ```
3. Configurer les clés API dans un fichier `.env` à la racine de `scripts/` :
   ```env
   NEWSAPI_KEY=votre_cle
   TAVILY_API_KEY=votre_cle
   ```

## Utilisation

Lancer une veille via la ligne de commande :
```bash
python scripts/news_fetcher.py "votre recherche" --days 1
```
