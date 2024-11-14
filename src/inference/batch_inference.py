from pathlib import Path
import pickle

import sklearn.ensemble
import sklearn.metrics
import typer
import pandas as pd
import sklearn
import json
from loguru import logger
from tqdm import tqdm

from src.entities.params import read_pipeline_params
from src.utils import get_sql_connection
app = typer.Typer()


@app.command()
def main(params_path: str):
    params = read_pipeline_params(params_path)
    conn = get_sql_connection(params)
    
    data_to_score = pd.read_sql_table(params.data_params.test_sql_tablename, conn)
    data_to_score.drop(['target'], axis=1, inplace=True)
    
    with open(params.train_params.model_path, 'rb') as fin:
        model = pickle.load(fin)
        
    data_to_score['predict'] = model.predict_proba(data_to_score)[:, 1]
    data_to_score.to_sql(con=conn, name="batch_inference_data", if_exists='append', index=False)
    logger.info(f"Upload batch inference data")


if __name__ == "__main__":
    app()
