import typer
import yaml
from loguru import logger

app = typer.Typer()


@app.command()
def main(config_path: str):
    """
    Function for generating features on your dataset
    """
    with open(config_path, 'r') as fin:
        config = yaml.safe_load(fin)
    logger.info("Loaded config with values")
    logger.info(config)
    logger.debug(f"Number of estimators equal: {config['train_params']['n_estimators']}")


if __name__ == "__main__":
    app()
