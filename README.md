# MedWatch - AI Intelligence Skill pour la Veille Médicale

MedWatch n'est pas qu'une collection de scripts ; c'est un **Skill agentique** conçu pour transformer un assistant IA en un analyste spécialisé en intelligence médicale. Il combine une couche d'outils performants (Tools) avec une couche d'instructions stratégiques (Skill) pour produire une veille structurée, exhaustive et pertinente.

## 🧠 Architecture du Skill

Le projet repose sur deux piliers complémentaires :

1.  **La Couche d'Intelligence (`SKILL.md`)** : Elle définit le "cerveau" de l'assistant. Elle contient les critères de sélection, les principes d'exhaustivité (priorisation des sources nationales, analyse des enjeux socio-professionnels) et les protocoles de synthèse.
2.  **La Couche d'Exécution (`scripts/`)** : Elle constitue la "boîte à outils" de l'IA. Elle permet d'interroger simultanément plusieurs moteurs (NewsAPI, Tavily, Google News RSS) et de normaliser les données brutes avant analyse.

## 🚀 Fonctionnalités Clés

- **Pilotage par IA** : Contrairement à un simple agrégateur de flux, MedWatch utilise le raisonnement de l'IA pour catégoriser les articles par axes stratégiques (Clinique, Institutionnel, Socio-professionnel, Innovation).
- **Orchestration Parallèle** : Récupération ultra-rapide des données via une pipeline multithreadée.
- **Analyse d'Exhaustivité** : Instructions spécifiques pour garantir qu'aucune enquête de fond (ex: Le Monde, Le Figaro) ne soit omise, même en l'absence de mots-clés techniques.
- **Rapports Actionnables** : Génération automatique de revues de presse en Markdown, prêtes à être consommées ou partagées.

## 🛠️ Composants Techniques (Tools)

- `news_fetcher.py` : L'interface de commande pour déclencher la récolte de données.
- `pipeline.py` : L'orchestrateur qui gère les connecteurs en parallèle.
- `google_news_connector.py` : Connecteur optimisé pour les flux RSS Google News (avec décodage HTML natif).
- `models.py` : Schémas Pydantic garantissant l'intégrité des données transmises à l'IA.

## 📦 Installation et Usage

### 1. Environnement
```bash
python -m venv scripts/.venv
pip install -r scripts/requirements.txt
```

### 2. Configuration
Créez un fichier `scripts/.env` avec vos clés API :
```env
NEWSAPI_KEY=xxx
TAVILY_API_KEY=xxx
```

### 3. Déclenchement
L'IA utilise cet outil de la manière suivante :
```bash
python scripts/news_fetcher.py "thématique de veille" --days 1
```

---
*Ce projet est une démonstration de la puissance des assistants agentiques lorsqu'ils sont dotés d'outils spécialisés et de directives métier claires.*
