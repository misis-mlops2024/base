from pathlib import Path

import sklearn.datasets
import sklearn.model_selection
import typer
import sklearn
import pandas as pd
import numpy as np
import sqlalchemy
from loguru import logger
from tqdm import tqdm
from src.entities.params import read_pipeline_params
from src.utils import get_sql_connection
from clearml import Task, Dataset

app = typer.Typer()


@app.command()
def main(params_path: str):
    """
    Function to generate dataset
    """
    params = read_pipeline_params(params_path)
    
    task = Task.init(project_name="my project", task_name="my task")
    
    # Создаем 
    dataset = Dataset.create(
        dataset_name='my dataset',
        dataset_project="my project",
    )
    
    X, y = sklearn.datasets.make_classification(
        n_samples=params.data_params.n_samples, n_features=params.data_params.n_features
    )
    data = pd.DataFrame(np.hstack([X, y.reshape(-1, 1)]))
    data.columns = [f"feat_{i}" for i in range(data.shape[-1])]
    data = data.rename({f"feat_{data.shape[-1] - 1}": "target"}, axis=1)
    logger.info(f"Got data with shape: {data.shape}")

    train, test = sklearn.model_selection.train_test_split(
        data, test_size=params.data_params.test_size, random_state=params.random_state
    )
    logger.info(f"Split data into train ({train.shape}) and test ({test.shape})")

    train.to_csv(params.data_params.train_data_path, index=False)
    logger.info(f"Save train sample to the path: {params.data_params.train_data_path}")

    test.to_csv(params.data_params.test_data_path, index=False)
    logger.info(f"Save test sample to the path: {params.data_params.test_data_path}")
    
    # Добавляем файлы в ClearMl Dataset (можно делать аналогично через CLI clearml-data)
    dataset.add_files(path=params.data_params.train_data_path)
    dataset.add_files(path=params.data_params.test_data_path)
    dataset.upload()
    dataset.finalize()


if __name__ == "__main__":
    app()
