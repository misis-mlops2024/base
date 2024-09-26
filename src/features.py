import typer
from loguru import logger
from tqdm import tqdm

from src.entities.params import read_pipeline_params

app = typer.Typer()


@app.command()
def main(params_path: str):
    """
    Function for generating features on your dataset
    """
    params = read_pipeline_params(params_path)


if __name__ == "__main__":
    app()
