---
name: medwatch
description: Recherche et résume l'actualité récente concernant les médecins via NewsAPI à partir de requêtes en langage naturel.
user-invocable: true
---

# medwatch

Ce skill permet aux journalistes de réaliser une veille automatisée sur des sujets de santé ou relatifs au système de soins concernant les médecins, en transformant une intention de recherche en une revue de presse structurée.

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

Le rapport doit être structuré en **3 sections dans l'ordre suivant** (supprime la mention "Section x" dansle rapport final):

---

### Section 1 — En-tête de synthèse

```
# Veille {sujet} — {date_du_jour en toutes lettres}

**Requête** : `{query}` | **Période** : {N} jour(s) | **Sources** : NewsAPI ({N} articles retenus), Tavily ({N} articles retenus)
```

> Si des erreurs ont été détectées lors de l'exécution, les mentionner ici sous forme de bloc citation.
> Si les résultats sont peu pertinents, suggérer ici une requête alternative.

---

### Section 2 — Articles retenus

Répéter le gabarit suivant pour chaque article retenu :

```
### [TITRE DE L'ARTICLE EN MAJUSCULES]
- **Source** : {source_name}
- **Date** : {date_formatée}
- **Résumé** : {synthèse de 3 à 4 lignes}
- **Lien** : {url}
```

---

### Section 3 — Articles non retenus
Cette section sert à justifier l'écartement de certains résultats pour garantir la crédibilité de la veille. Pour cahque article, n'oublie pas de metionner le titre, la source et l'URL.

```
## Articles non retenus

**Doublons** *(Articles traitant du même sujet exact avec une information identique)*
- {titre_court} — {source} — ({url})

**Santé sans mention des médecins** *(Articles médicaux généraux ne ciblant pas la profession ou le système de soins)*
- {titre_court} — {source} — ({url})

**Justice / Faits divers** *(Sauf si implication déontologique majeure du médecin)*
- {titre_court} — {source} — ({url})

**Hors sujet** *(Sujets n'ayant aucun lien avec la santé ou la pratique médicale)*
- {titre_court} — {source} — ({url})
```

> N'afficher que les catégories non vides. Les articles de sources majeures (Le Monde, etc.) ne doivent se trouver ici que s'ils sont réellement hors sujet ou doublons.

---

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