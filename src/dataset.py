from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

app = typer.Typer()


@app.command()
def main(input_path: Path, output_path: Path):
    """
    Function to generate dataset
    """
    pass


if __name__ == "__main__":
    app()
