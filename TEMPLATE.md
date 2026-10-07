Le rapport doit être structuré en **3 sections dans l'ordre suivant** (supprime la mention "Section x" dans le rapport final) :

---

### Section 1 — En-tête de synthèse

```
# Veille {sujet} — {date_du_jour en toutes lettres}

**Profil** : {socio-professionnel ou médical} | **Requête** : `{query}` | **Période** : {N} jour(s) | **Sources** : {liste des sources activées avec nombre d'articles retenus}
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

Cette section sert à justifier l'écartement de certains résultats pour garantir la crédibilité de la veille. Pour chaque article, mentionner le titre, la source et l'URL.

Les catégories de non-rétention dépendent du profil. N'afficher que les catégories non vides.

#### Profil socio-professionnel

```
## Articles non retenus

**Doublons** *(Articles traitant du même sujet exact avec une information identique)*
- {titre_court} — {source} — ({url})

**Recherche fondamentale** *(Études ou publications sans impact direct sur le système de soins ou la profession)*
- {titre_court} — {source} — ({url})

**Justice / Faits divers** *(Sauf si implication déontologique majeure)*
- {titre_court} — {source} — ({url})

**Hors sujet** *(Sujets n'ayant aucun lien avec la santé ou le système de soins)*
- {titre_court} — {source} — ({url})
```

#### Profil médical

```
## Articles non retenus

**Doublons** *(Articles traitant du même sujet exact avec une information identique)*
- {titre_court} — {source} — ({url})

**Actualité socio-professionnelle** *(Articles sur la profession ou la politique de santé sans dimension clinique ou scientifique)*
- {titre_court} — {source} — ({url})

**Faits divers** *(Sauf si implication de santé publique)*
- {titre_court} — {source} — ({url})

**Hors sujet** *(Sujets n'ayant aucun lien avec la médecine ou la santé publique)*
- {titre_court} — {source} — ({url})
```

> Les articles de sources de référence (médias nationaux, revues médicales) ne doivent se trouver ici que s'ils sont réellement hors sujet ou doublons.

---
