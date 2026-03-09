from typing import List, Literal, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class Article(BaseModel):
    # Strip enlève les espaces inutiles, min_length empêche les titres vides
    titre: str = Field(
        ...,
        strip_whitespace=True,
        min_length=1,
        max_length=500,
        description="Le titre de l'article",
    )

    url: HttpUrl = Field(..., description="Le lien hypertexte vers l'article original")

    date_publication: str = Field(
        ..., description="Date de publication au format YYYY-MM-DD ou ISO"
    )

    source: str = Field(
        ..., strip_whitespace=True, description="Nom du média ou du site web"
    )

    # Validation stricte du moteur autorisé
    moteur: Literal["NewsAPI", "Tavily", "PubMed", "GoogleNews"] = Field(
        ..., description="Le moteur ayant extrait la donnée"
    )

    # On garantit que l'extrait ne sera jamais silencieusement vide, et on le coupe s'il est trop long plus tard
    extrait: str = Field(
        ...,
        strip_whitespace=True,
        max_length=2000,
        description="L'extrait ou le résumé du contenu",
    )

    score: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Score de pertinence entre 0 et 1"
    )

    # Exemple de validateur (nettoyeur de texte automatique)
    @field_validator("extrait")
    @classmethod
    def clean_text(cls, v: str) -> str:
        # Pydantic va exécuter cette fonction à chaque création d'un article.
        # Ici on remplace les retours à la ligne, tabulations ou espaces multiples par un seul espace
        import re

        if v is None:
            return ""
        return re.sub(r"\s+", " ", v).strip()


class ReponseGlobale(BaseModel):
    requete: str = Field(..., description="Les mots-clés recherchés")
    statut: str = Field(default="succès", description="'succès' ou 'erreur'")
    nombre_articles_trouves: int = Field(
        default=0, description="Le total d'articles après déduplication"
    )
    nombre_articles_par_source: dict[str, int] = Field(
        default_factory=dict, description="Le nombre d'articles par moteur/source"
    )
    articles: List[Article] = Field(
        default_factory=list, description="La liste des articles trouvés"
    )
    message_erreur: Optional[str] = Field(
        None, description="Le détail de l'erreur en cas de problème"
    )
