from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from src.config import PROCESSED_DATA_DIR

app = typer.Typer()


@app.command()
def main(input_path: Path, output_path: Path):
    """
    Function for generating features on your dataset
    """
    pass


if __name__ == "__main__":
    app()
