---
name: medwatch
description: Recherche et résume l'actualité médicale récente via NewsAPI à partir de requêtes en langage naturel.
---

# medwatch

Ce skill permet aux journalistes de réaliser une veille automatisée sur des sujets de santé concernant les médecins, en transformant une intention de recherche en une revue de presse structurée.

## Usage

Utilisez ce skill lorsque l'utilisateur demande :
- Une veille sur l'actualité socio-professionnelle des médecins (ex: "Quelles sont les dernières actualités concernant les médecins ?").
- Une veille sur une pathologie ou un traitement (ex: "Quoi de neuf sur le diabète ?").
- Une liste d'articles parus sur une période précise (ex: "Les actus de ces 3 derniers jours sur l'ARN messager").
- Un résumé des dernières publications d'une source spécifique si mentionnée.

## Tools

Le skill s'appuie sur la commande suivante définie dans le frontmatter :
- `scripts/.venv/bin/python3 scripts/news_fetcher.py "{query}" {days}`
- `{query}` : Mots-clés extraits et optimisés par Claude.
- `{days}` : Nombre de jours (par défaut 1 si non spécifié).

## Instructions

### 1. Prétraitement de la requête
Avant d'exécuter la commande, traduisez l'intention de l'utilisateur en une requête de recherche efficace. 
- Utilisez des opérateurs OR si nécessaire (ex: "cancer du poumon OR oncologie thoracique").
- Nettoyez les mots inutiles ("donne moi", "est-ce que tu peux trouver").

### 2. Exécution et Analyse
- Lancez la commande Python.
- Si le script retourne un JSON vide, informez l'utilisateur qu'aucune actualité n'a été trouvée pour cette période et suggérez d'élargir la recherche.
- Si le script retourne un objet JSON avec une clé "error", informez l'utilisateur du problème technique (clé API invalide, problème réseau) et suggérez de réessayer.
- En cas de succès, analysez chaque article pour vérifier sa pertinence vis à vis de la requête de l'utilisateur.

### 3. Rédaction des résumés
Rédigez pour chaque article un résumé de 3 à 4 lignes maximum.
- **Ton** : Professionnel, factuel.
- **Contenu** : Indiquez quelle est l'information essentielle et en quoi cela peut intéresser les médecins.

## Output Format

Affichez les résultats sous cette forme :

### [TITRE DE L'ARTICLE EN MAJUSCULES]
- **Source** : {source_name}
- **Date** : {date_formatée}
- **Résumé** : {votre_synthèse_rédigée}
- **Lien** : [Consulter l'article]({url})

---

## Examples

**Journaliste** : "Fais-moi une veille sur la maladie de Crohn depuis hier."
**Action** : Claude identifie `query="maladie de Crohn"` et `days=1`.
**Exécution** : `python3 news_fetcher.py "maladie de Crohn" 1`
**Résultat** : Affiche les articles formatés selon le standard.

**Journaliste** : "Quelles sont les alertes de l'ANSM sur les 7 derniers jours ?"
**Action** : Claude identifie `query="ANSM OR alerte médicament"` et `days=7`.
**Exécution** : `python3 news_fetcher.py "ANSM OR alerte médicament" 7`

**Journaliste** : "Fais-moi une veille sur l'actualité socio-pro des médecins au cours des 24 dernières heures."
**Action** : Claude identifie `query="médecin santé"` et `days=1`.
**Exécution** : `python3 news_fetcher.py "médecin santé" 1`
**Résultat** : Affiche les articles formatés selon le standard.