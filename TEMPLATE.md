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