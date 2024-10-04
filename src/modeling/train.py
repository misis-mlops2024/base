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
    con = get_sql_connection(params)
    train = pd.read_sql_table(params.data_params.train_sql_tablename, con)
    X_train = train.drop("target", axis=1)
    y_train = train["target"].values.reshape(-1, 1)

    test = pd.read_sql_table(params.data_params.test_sql_tablename, con)
    X_test = test.drop("target", axis=1)
    y_test = test["target"].values.reshape(-1, 1)

    model = sklearn.ensemble.RandomForestClassifier(n_estimators=params.train_params.n_estimators)
    model.fit(X_train, y_train)
    logger.info(f"Learn model {model}")

    y_test_pred = model.predict_proba(X_test)[:, 1]
    roc_auc = sklearn.metrics.roc_auc_score(y_test, y_test_pred)
    logger.info(f"Got ROC-AUC {roc_auc:.3f}")

    metrics = {"roc-auc": roc_auc}

    with open(params.train_params.model_path, "wb") as fin:
        pickle.dump(model, fin)
    logger.info(f"Saved model to path {params.train_params.model_path}")

    with open(params.train_params.metrics_path, "w") as fin:
        json.dump(metrics, fin)
    logger.info(f"Saved metrics to path {params.train_params.metrics_path}")


if __name__ == "__main__":
    app()
