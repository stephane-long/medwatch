---
name: medwatch
description: "Utiliser quand l’utilisateur demande une veille d’actualité médicale, une revue de presse, ou des informations récentes sur les médecins, le système de soins, une pathologie, un traitement, un médicament, l’ANSM, ou une source nommée. Agrège plusieurs sources (NewsAPI, Tavily, Google News RSS), filtre les résultats par pertinence et génère un rapport Markdown structuré."
user-invocable: true
---

# medwatch

Ce skill transforme une demande de veille médicale en revue de presse structurée pour des journalistes. Il collecte des articles issus de plusieurs sources, aide à évaluer leur pertinence pour les médecins et le système de soins, puis produit un rapport Markdown exploitable par une rédaction.

## Usage

Utilisez ce skill lorsque l'utilisateur demande :
- Une veille sur l'actualité socio-professionnelle des médecins (ex: "Quelles sont les dernières actualités concernant les médecins ?").
- Une veille sur une pathologie ou un traitement (ex: "Quoi de neuf sur le diabète ?").
- Une liste d'articles parus sur une période précise (ex: "Les actus de ces 3 derniers jours sur l'ARN messager").
- Un résumé des dernières publications d'une source spécifique si mentionnée.

## Tools

Le skill s'appuie sur la commande suivante (à exécuter via l'interpréteur Python de l'environnement virtuel local) :
- `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "{query}" --days {days}`

> [!TIP]
> **Chemin du VENV** : Localisez l'exécutable Python dans `scripts/.venv/Scripts/python.exe` (Windows) ou `scripts/.venv/bin/python` (macOS/Linux).

## Instructions

### 1. Prétraitement de la requête
Avant d'exécuter la commande, traduisez l'intention de l'utilisateur en une requête de recherche efficace. 
- Utilisez des opérateurs OR si nécessaire (ex: "cancer du poumon OR oncologie thoracique").
- Nettoyez les mots inutiles ("donne moi", "est-ce que tu peux trouver").

### 2. Exécution et Analyse
- Lancez la commande Python.
- Si le script retourne un JSON vide, informez l'utilisateur qu'aucune actualité n'a été trouvée pour cette période et suggérez d'élargir la recherche.
- Si le script retourne un objet JSON avec une clé "error", informez l'utilisateur du problème technique (clé API invalide, problème réseau) et suggérez de réessayer.
- En cas de succès, analysez chaque article pour vérifier sa pertinence.
- **Principe d'exhaustivité** : Ne soyez pas trop restrictif. Un article est pertinent s'il traite de la pratique médicale, de la démographie, de l'éthique, de la formation ou des conditions d'exercice.
- **Priorité aux sources de référence** : Un reportage de fond ou une enquête d'un média national (ex: Le Monde, Le Figaro, Les Échos) doit TOUJOURS être retenu s'il concerne le système de santé, même s'il n'est pas purement clinique.
- **Diversité des sujets** : Assurez-vous de couvrir les différents axes : institutionnel, clinique, socio-professionnel et innovation.

### 3. Rédaction des résumés
Rédigez pour chaque article un résumé de 3 à 4 lignes maximum.
- **Ton** : Professionnel, factuel, pas de jugement.
- **Contenu** : Indiquez quelle est l'information essentielle et en quoi cela peut intéresser les médecins.

## Output Format

**ACTION OBLIGATOIRE** : Vous DEVEZ générer et enregistrer ce rapport dans un fichier physique `reports/{query_sanitisée}_{date_du_jour}.md` (remplacez les espaces et caractères spéciaux par `_`). Une fois le fichier créé, confirmez son emplacement exact à l'utilisateur.

Le rapport doit être structuré en suivant les instructions du fichier `TEMPLATE.md`.



## Examples

**Journaliste** : "Fais-moi une veille sur la maladie de Crohn depuis hier."
**Action** : L'assistant identifie `query="maladie de Crohn"` et `days=1`.
**Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "maladie de Crohn" --days 1`
**Résultat** : Affiche les articles formatés selon le standard.

**Journaliste** : "Quelles sont les alertes de l'ANSM sur les 7 derniers jours ?"
**Action** : L'assistant identifie `query="ANSM OR alerte médicament"` et `days=7`.
**Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "ANSM OR alerte médicament" --days 7`

**Journaliste** : "Fais-moi une veille sur l'actualité socio-pro des médecins au cours des 24 dernières heures."
**Action** : L'assistant identifie `query="médecin santé"` et `days=1`.
**Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "médecin santé" --days 1`
**Résultat** : Affiche les articles formatés selon le standard.