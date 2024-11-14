import typer
import yaml
from loguru import logger

from src.entities.params import read_pipeline_params

app = typer.Typer()


@app.command()
def main(config_path: str):
    """
    Function for generating features on your dataset
    """
    config = read_pipeline_params(config_path)
    logger.info("Loaded config with values")
    logger.info(config)
    logger.debug(f"Number of estimators equal: {config.train_params.n_estimators}")


if __name__ == "__main__":
    app()
