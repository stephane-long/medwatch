import typer
from dotenv import load_dotenv
from models import ReponseGlobale
from pipeline import run_pipeline

load_dotenv()

app = typer.Typer(help="Application MedWatch pour la veille d'actualité")


@app.command()
def fetch(
    query: str = typer.Argument(..., help="Les mots-clés de la recherche"),
    days: int = typer.Option(
        1,
        "--days",
        "-d",
        help="Nombre de jours dans le passé à rechercher (ex: 1 pour 24h)",
    ),
):
    """
    Lance une recherche d'actualités sur différentes sources (NewsAPI, Tavily)
    et les formate pour Claude.
    """
    try:
        # Exécute l'orchestrateur central
        reponse: ReponseGlobale = run_pipeline(query, days)

        # Affiche le résultat avec la conversion JSON stricte générée explicitement par Pydantic
        # On utilise print et non typer.echo ici pour que Claude puisse lire le JSON brut de stdout
        print(reponse.model_dump_json(indent=2))

    except Exception as e:
        # Si le système s'effondre pour des raisons inattendues,
        # on garantit un format de sortie JSON d'erreur propre pour Claude
        erreur_globale = ReponseGlobale(
            requete=query, statut="erreur", message_erreur=str(e)
        )
        print(erreur_globale.model_dump_json(indent=2))


if __name__ == "__main__":
    app()
