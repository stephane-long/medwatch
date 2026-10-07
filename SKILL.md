---
name: medwatch
description: "Utiliser quand l'utilisateur demande une veille d'actualité médicale, une revue de presse, ou des informations récentes sur les médecins, le système de soins, une pathologie, un traitement, un médicament, l'ANSM, ou une source nommée. Agrège plusieurs sources selon le profil (socio-pro ou médical), filtre les résultats par pertinence et génère un rapport Markdown structuré."
user-invocable: true
---

# medwatch

Ce skill transforme une demande de veille médicale en revue de presse structurée pour les journalistes du Quotidien du Médecin. Il dessert deux équipes aux centres d'intérêt distincts :

- **Équipe socio-professionnelle** : politique de santé, relations médecins / assurance-maladie, sécurité sociale, démographie médicale, conditions d'exercice
- **Équipe médicale** : recherche médicale, pratique clinique, santé publique, pharmacovigilance, revues médicales

Le skill adapte ses sources, ses critères de pertinence et ses catégories de tri selon le profil choisi.

## Usage

Utilisez ce skill lorsque l'utilisateur demande :
- Une veille sur l'actualité socio-professionnelle des médecins (ex: "Fais-moi la veille d'actu").
- Une veille sur la recherche médicale ou la santé publique (ex: "Quoi de neuf en médecine ?").
- Une liste d'articles parus sur une période précise (ex: "Les actus de ces 3 derniers jours sur l'ARN messager").
- Un résumé des dernières publications d'une source spécifique si mentionnée.

## Tools

Le skill s'appuie sur la commande suivante (à exécuter via l'interpréteur Python de l'environnement virtuel local) :
- `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "{query}" --days {days} --profile {profile}`

Le paramètre `--profile` accepte deux valeurs :
- `sociopro` : active NewsAPI, Tavily, Google News et ANSM
- `medical` : active JAMA et ANSM

> [!TIP]
> **Chemin du VENV** : Localisez l'exécutable Python dans `scripts/.venv/Scripts/python.exe` (Windows) ou `scripts/.venv/bin/python` (macOS/Linux).

## Instructions

### 0. Clarification du profil (OBLIGATOIRE)

**Avant tout prétraitement**, déterminez le profil de veille. Si la requête du journaliste est générique ou ambiguë (ex: "fais-moi la veille d'actu", "quoi de neuf ?"), vous DEVEZ lui poser la question :

> Votre veille porte sur l'actualité **socio-professionnelle** (politique de santé, assurance-maladie, démographie médicale, conditions d'exercice...) ou sur l'actualité **médicale** (recherche, pratique clinique, santé publique, pharmacovigilance...) ?

Si la requête est explicitement orientée (ex: "les dernières publications JAMA", "la convention médicale"), déduisez le profil sans poser la question :
- Mots-clés socio-pro : médecins, convention, assurance maladie, CNAM, démographie, exercice, hôpital, sécurité sociale, politique de santé
- Mots-clés médicaux : étude, essai clinique, traitement, pathologie, recherche, JAMA, Lancet, santé publique, épidémiologie

### 1. Prétraitement de la requête (OBLIGATOIRE)

**Règle fondamentale** : Toute requête brute ou générale DOIT être enrichie avec des termes connexes avant exécution. Les patterns d'enrichissement dépendent du profil.

#### A. Heuristiques pour déterminer si enrichissement est nécessaire

| Type de requête | Exemples | Action |
|---|---|---|
| **Métier/profession brut** | "médecins", "infirmiers" | Enrichir avec contexte professionnel |
| **Pathologie simple** | "diabète", "cancer" | Enrichir avec synonymes cliniques et traitements |
| **Organisme/institution** | "ANSM", "HAS" | Enrichir avec domaine d'activité |
| **Traitement générique** | "vaccination", "antibiothérapie" | Enrichir avec contextes spécifiques |
| **Concept brut** | "télémédecine", "santé" | Enrichir avec déclinaisons |
| **Requête très spécifique** | "fracture du tibia chez l'enfant", "loi Kouchner" | Peut rester telle quelle |

#### B. Patterns d'enrichissement par profil

##### Profil socio-professionnel

**Actualité socio-professionnelle**
```
"médecins" → "médecins OR santé OR hôpital OR système de soins"
"convention médicale" → "convention médicale OR assurance maladie OR tarifs médicaux OR négociations"
```

**Organismes et autorités**
```
"ANSM" → "ANSM OR alerte médicament OR sécurité sanitaire"
"HAS" → "HAS OR recommandations cliniques OR bonnes pratiques"
```

**Politique et systèmes de santé**
```
"réforme sanitaire" → "réforme sanitaire OR système de santé OR politique de santé OR assurance maladie"
```

**Veille générique socio-pro** (quand le journaliste dit simplement "fais la veille")
```
"médecins OR système de soins OR hôpital OR politique de santé OR assurance maladie"
```

##### Profil médical

**Pathologies et conditions médicales**
```
"diabète" → "diabète OR hyperglycémie OR traitement du diabète OR insuline"
"cancer" → "cancer OR oncologie OR chimiothérapie OR immunothérapie"
```

**Recherche et essais cliniques**
```
"essai clinique" → "essai clinique OR étude randomisée OR méta-analyse OR cohorte"
"immunothérapie" → "immunothérapie OR anti-PD1 OR checkpoint immunitaire OR CAR-T"
```

**Santé publique**
```
"vaccination" → "vaccination OR couverture vaccinale OR calendrier vaccinal OR pharmacovigilance"
"épidémiologie" → "épidémiologie OR incidence OR prévalence OR surveillance sanitaire"
```

**Veille générique médicale** (quand le journaliste dit simplement "fais la veille")
```
"recherche médicale OR essai clinique OR santé publique OR thérapeutique OR pharmacovigilance"
```

**Innovations et technologies** (commun aux deux profils)
```
"télémédecine" → "télémédecine OR visioconférence médicale OR consultations à distance"
"intelligence artificielle en santé" → "intelligence artificielle OR machine learning OR algorithme médical OR diagnostic IA"
```

#### C. Processus de prétraitement (étape par étape)

1. **Identifier le profil** : socio-pro ou médical (cf. étape 0)
2. **Identifier le type de requête** : métier ? pathologie ? organisme ? technologie ? politique ?
3. **Consulter les patterns du profil** : déterminer si enrichissement est nécessaire
4. **Appliquer le pattern approprié** : 2-4 termes connexes via OR, pertinents pour le profil
5. **Nettoyer les mots inutiles** : "donne moi", "trouve", "peux-tu"
6. **Vérifier la cohérence** : tous les termes doivent converger vers le même sujet

#### D. Checklist avant exécution

- [ ] Le profil a été déterminé (sociopro ou medical) ?
- [ ] La requête a-t-elle au moins 2-3 concepts liés via OR (sauf si très spécifique) ?
- [ ] Les termes sont-ils cohérents avec le profil choisi ?
- [ ] La requête contient-elle des mots inutiles à supprimer ?
- [ ] Les termes capturent-ils synonymes, variantes et domaines connexes ?

### 2. Exécution et Analyse

- Lancez la commande Python avec le `--profile` correspondant.
- Si le script retourne un JSON vide, informez l'utilisateur qu'aucune actualité n'a été trouvée pour cette période et suggérez d'élargir la recherche.
- Si le script retourne un objet JSON avec `statut` égal à `"erreur"`, consultez le champ `message_erreur` pour identifier le problème technique (clé API invalide, problème réseau) et informez l'utilisateur en lui suggérant de réessayer.
- En cas de succès, analysez chaque article pour vérifier sa pertinence **selon le profil**.

#### Critères de pertinence par profil

**Profil socio-professionnel** — un article est pertinent s'il traite de :
- La profession médicale, la démographie, l'éthique ou la formation des médecins
- La politique de santé, les réformes, le financement du système de soins
- Les relations conventionnelles entre médecins et assurance maladie
- Les conditions d'exercice (installation, rémunération, permanence des soins)
- Les alertes ANSM ayant un impact sur la pratique quotidienne

**Profil médical** — un article est pertinent s'il traite de :
- Résultats d'études cliniques ou d'essais thérapeutiques
- Nouvelles thérapeutiques, AMM, recommandations de sociétés savantes
- Épidémiologie, surveillance sanitaire, données de santé publique
- Pharmacovigilance, alertes sur les médicaments ou dispositifs médicaux
- Innovations diagnostiques ou thérapeutiques

#### Règles communes aux deux profils

- **Exhaustivité des listes du rapport (obligatoire)** : toutes les listes du rapport doivent être exhaustives par rapport au JSON brut. Aucun article ne doit être omis.
- **Aucun échantillonnage** : n'utilisez jamais "quelques exemples" dans les sections d'articles non retenus. Listez tous les articles concernés dans leur catégorie.
- **Règle de partition** : chaque article du JSON doit apparaître exactement une fois, soit dans "Articles retenus", soit dans une catégorie de "Articles non retenus".
- **Contrôle final obligatoire** : avant d'enregistrer le rapport, vérifiez que le total des entrées listées (retenus + non retenus) est égal à `nombre_articles_trouves` du JSON.
- **Priorité aux sources de référence** :
  - Socio-pro : médias nationaux (Le Monde, Le Figaro, Les Échos) + presse spécialisée (Le Quotidien du Médecin, APMnews)
  - Médical : revues médicales (JAMA, Lancet, NEJM, BMJ) + médias nationaux si dimension santé publique
- **Diversité des sujets** : couvrir les différents axes du profil concerné.

### 3. Rédaction des résumés
Rédigez pour chaque article retenu un résumé de 3 à 4 lignes maximum.
- **Ton** : Professionnel, factuel, pas de jugement.
- **Contenu** : Indiquez quelle est l'information essentielle et en quoi elle concerne le domaine du profil choisi.

## Output Format

**ACTION OBLIGATOIRE** : Vous DEVEZ générer et enregistrer ce rapport dans un fichier physique `reports/{query_sanitisée}_{date_du_jour}.md` (remplacez les espaces et caractères spéciaux par `_`). Une fois le fichier créé, confirmez son emplacement exact à l'utilisateur.

Le rapport doit être structuré en suivant les instructions du fichier `TEMPLATE.md`.

## Examples

**Exemple 1 — Veille générique socio-pro**
- **Journaliste** : "Fais-moi la veille d'actu."
- **Clarification** : "Socio-pro ou médical ?" → "Socio-pro"
- **Requête enrichie** : `"médecins OR système de soins OR hôpital OR politique de santé OR assurance maladie"`
- **Paramètres** : `days=1`, `profile=sociopro`
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "médecins OR système de soins OR hôpital OR politique de santé OR assurance maladie" --days 1 --profile sociopro`

**Exemple 2 — Veille générique médicale**
- **Journaliste** : "Fais la veille du jour."
- **Clarification** : "Socio-pro ou médical ?" → "Médical"
- **Requête enrichie** : `"recherche médicale OR essai clinique OR santé publique OR thérapeutique OR pharmacovigilance"`
- **Paramètres** : `days=1`, `profile=medical`
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "recherche médicale OR essai clinique OR santé publique OR thérapeutique OR pharmacovigilance" --days 1 --profile medical`

**Exemple 3 — Alerte pharmacovigilance (profil déduit)**
- **Journaliste** : "Quelles sont les alertes de l'ANSM sur les 7 derniers jours ?"
- **Profil déduit** : sociopro (ANSM = organisme de régulation)
- **Requête enrichie** : `"ANSM OR alerte médicament OR sécurité sanitaire"`
- **Paramètres** : `days=7`, `profile=sociopro`
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "ANSM OR alerte médicament OR sécurité sanitaire" --days 7 --profile sociopro`

**Exemple 4 — Pathologie (profil déduit)**
- **Journaliste** : "Quoi de neuf sur le diabète ?"
- **Profil déduit** : medical (pathologie)
- **Requête enrichie** : `"diabète OR hyperglycémie OR traitement du diabète OR insuline"`
- **Paramètres** : `days=1`, `profile=medical`
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "diabète OR hyperglycémie OR traitement du diabète OR insuline" --days 1 --profile medical`

**Exemple 5 — Innovation technologique (profil explicite)**
- **Journaliste** : "Qu'est-ce qui se passe avec la télémédecine ?"
- **Clarification** : "Socio-pro ou médical ?" → Le journaliste choisit
- **Requête enrichie** : `"télémédecine OR visioconférence médicale OR consultations à distance OR e-santé"`
- **Paramètres** : `days=2`, `profile=sociopro` (ou `medical` selon la réponse)
- **Exécution** : `[VENV_PYTHON] -X utf8 scripts/news_fetcher.py "télémédecine OR visioconférence médicale OR consultations à distance OR e-santé" --days 2 --profile sociopro`
