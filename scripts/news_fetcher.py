import io
import sys

import typer
from dotenv import load_dotenv
from models import ReponseGlobale
from pipeline import run_pipeline

# Forçage de l'UTF-8 pour la sortie standard, utile sur Windows
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

load_dotenv()

app = typer.Typer(help="Application MedWatch pour la veille d'actualité")


@app.command()
def fetch(
    query: str = typer.Argument(..., help="Les mots-clés de la recherche"),
    days: int = typer.Option(
        1,
        "--days",
        "-d",
        help="Nombre de jours calendaires à inclure (ex: 1 = depuis minuit de J-1)",
    ),
    profile: str = typer.Option(
        "sociopro",
        "--profile",
        "-p",
        help="Profil de veille : sociopro (presse + ANSM) ou medical (JAMA + ANSM)",
    ),
):
    """
    Lance une recherche d'actualités sur différentes sources selon le profil choisi
    et les formate pour Claude.
    """
    if profile not in ("sociopro", "medical"):
        typer.echo(f"Profil invalide : {profile}. Utilisez 'sociopro' ou 'medical'.", err=True)
        raise typer.Exit(code=1)

    try:
        # Exécute l'orchestrateur central
        reponse: ReponseGlobale = run_pipeline(query, days, profile)

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
