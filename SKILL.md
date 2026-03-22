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

### 1. Prétraitement de la requête (OBLIGATOIRE)

**Règle fondamentale** : Toute requête brute ou générale DOIT être enrichie avec des termes connexes avant exécution. Une requête simple à un seul concept est rarement exhaustive pour une veille d'actualité destinée aux journalistes.

#### A. Heuristiques pour déterminer si enrichissement est nécessaire

| Type de requête | Exemples | Action |
|---|---|---|
| **Métier/profession brut** | "médecins", "infirmiers" | ➕ Enrichir avec contexte professionnel |
| **Pathologie simple** | "diabète", "cancer" | ➕ Enrichir avec synonymes cliniques et traitements |
| **Organisme/institution** | "ANSM", "HAS" | ➕ Enrichir avec domaine d'activité |
| **Traitement générique** | "vaccination", "antibiothérapie" | ➕ Enrichir avec contextes spécifiques |
| **Concept brut** | "télémédecine", "santé" | ➕ Enrichir avec déclinaisons |
| **Requête très spécifique** | "fracture du tibia chez l'enfant", "loi Kouchner" | ✓ Peut rester telle quelle |

#### B. Patterns d'enrichissement par domaine

**Actualité socio-professionnelle des médecins**
```
❌ "médecins"
✓ "médecins OR santé OR hôpital OR système de soins"
```

**Pathologies et conditions médicales**
```
❌ "diabète"
✓ "diabète OR hyperglycémie OR traitement du diabète OR endocrinologie"

❌ "cancer"
✓ "cancer OR oncologie OR chimiothérapie OR radiothérapie"
```

**Organismes et autorités**
```
❌ "ANSM"
✓ "ANSM OR alerte médicament OR sécurité sanitaire"

❌ "HAS"
✓ "HAS OR recommandations cliniques OR bonnes pratiques"
```

**Innovations et technologies**
```
❌ "télémédecine"
✓ "télémédecine OR visioconférence médicale OR consultations à distance"

❌ "intelligence artificielle en santé"
✓ "intelligence artificielle OR machine learning OR algorithme médical OR diagnostic IA"
```

**Politique et systèmes de santé**
```
❌ "réforme sanitaire"
✓ "réforme sanitaire OR système de santé OR politique de santé OR assurance maladie"
```

#### C. Processus de prétraitement (étape par étape)

1. **Identifier le type de requête** : métier ? pathologie ? organisme ? technologie ? politique ?
2. **Consulter le tableau ci-dessus** : déterminer si enrichissement est nécessaire
3. **Appliquer le pattern approprié** : 2-4 termes connexes via OR, pertinents pour les journalistes santé
4. **Nettoyer les mots inutiles** : "donne moi", "trouve", "peux-tu"
5. **Vérifier la cohérence** : tous les termes doivent converger vers le même sujet

#### D. Checklist avant exécution

- [ ] La requête a-t-elle au moins 2-3 concepts liés via OR (sauf si très spécifique) ?
- [ ] Les termes couvrent-ils les angles clés pour les journalistes santé (pro, clinique, institution) ?
- [ ] La requête contient-elle des mots inutiles à supprimer ?
- [ ] Les termes sont-ils cohérents (pas de dérive hors du sujet) ?
- [ ] La requête captures-t-elle synonymes, variantes et domaines connexes ?

### 2. Exécution et Analyse
- Lancez la commande Python.
- Si le script retourne un JSON vide, informez l'utilisateur qu'aucune actualité n'a été trouvée pour cette période et suggérez d'élargir la recherche.
- Si le script retourne un objet JSON avec une clé "error", informez l'utilisateur du problème technique (clé API invalide, problème réseau) et suggérez de réessayer.
- En cas de succès, analysez chaque article pour vérifier sa pertinence.
- **Principe d'exhaustivité** : Ne soyez pas trop restrictif. Un article est pertinent s'il traite de la pratique médicale, de la démographie, de l'éthique, de la formation ou des conditions d'exercice.
- **Exhaustivité des listes du rapport (obligatoire)** : toutes les listes du rapport doivent être exhaustives par rapport au JSON brut. Aucun article ne doit être omis.
- **Aucun échantillonnage** : n'utilisez jamais "quelques exemples" dans les sections d'articles non retenus. Listez tous les articles concernés dans leur catégorie.
- **Règle de partition** : chaque article du JSON doit apparaître exactement une fois, soit dans "Articles retenus", soit dans une catégorie de "Articles non retenus".
- **Contrôle final obligatoire** : avant d'enregistrer le rapport, vérifiez que le total des entrées listées (retenus + non retenus) est égal à `nombre_articles_trouves` du JSON.
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

**Exemple 1 — Actualité socio-professionnelle (requête brute)**
- **Journaliste** : "Fais-moi une veille sur les médecins en ce moment."
- **Prétraitement** : Requête brute et générale → enrichir selon pattern métier
- **Requête enrichie** : `"médecins OR santé OR hôpital OR système de soins"`
- **Paramètres** : `days=1` (défaut : 1 jour)
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "médecins OR santé OR hôpital OR système de soins" --days 1`

**Exemple 2 — Alerte pharmacovigilance (requête partiellement enrichie)**
- **Journaliste** : "Quelles sont les alertes de l'ANSM sur les 7 derniers jours ?"
- **Prétraitement** : "ANSM" seul est trop restrictif → enrichir avec domaine d'activité
- **Requête enrichie** : `"ANSM OR alerte médicament OR sécurité sanitaire"`
- **Paramètres** : `days=7`
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "ANSM OR alerte médicament OR sécurité sanitaire" --days 7`

**Exemple 3 — Pathologie avec contexte clinique (requête brute)**
- **Journaliste** : "Quoi de neuf sur le diabète ?"
- **Prétraitement** : Pathologie générique → enrichir avec synonymes et traitements
- **Requête enrichie** : `"diabète OR hyperglycémie OR traitement du diabète OR insuline"`
- **Paramètres** : `days=1`
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "diabète OR hyperglycémie OR traitement du diabète OR insuline" --days 1`

**Exemple 4 — Maladie rare (requête très spécifique)**
- **Journaliste** : "Les dernières infos sur la maladie de Crohn depuis hier."
- **Prétraitement** : Condition clinique spécifique et nommée → suffisamment ciblée, enrichissement optionnel
- **Requête enrichie** : `"maladie de Crohn OR maladie inflammatoire de l'intestin"` (enrichissement léger)
- **Paramètres** : `days=1`
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "maladie de Crohn OR maladie inflammatoire de l'intestin" --days 1`

**Exemple 5 — Innovation technologique (requête brute)**
- **Journaliste** : "Qu'est-ce qui se passe avec la télémédecine ?"
- **Prétraitement** : Concept générique → enrichir avec déclinaisons
- **Requête enrichie** : `"télémédecine OR visioconférence médicale OR consultations à distance OR e-santé"`
- **Paramètres** : `days=2`
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "télémédecine OR visioconférence médicale OR consultations à distance OR e-santé" --days 2`