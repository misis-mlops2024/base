import pickle
import os

import sklearn.ensemble
import sklearn.metrics
import typer
import pandas as pd
import sklearn
import json
from loguru import logger
from tqdm import tqdm
from clearml import Task, Dataset
import joblib

from src.entities.params import read_pipeline_params
from src.utils import get_sql_connection

app = typer.Typer()


@app.command()
def main(params_path: str):
    params = read_pipeline_params(params_path)

    task = Task.init(project_name="my project", task_name="baseline")
    
    dataset_folder = Dataset.get(dataset_name='my dataset', dataset_project='my project').get_local_copy()
    task.set_progress(0)
    
    # Читаем данные
    train = pd.read_csv(os.path.join(dataset_folder, 'train.csv'))
    X_train = train.drop("target", axis=1)
    y_train = train["target"].values.reshape(-1, 1)
    task.set_progress(10)
    
    test = pd.read_csv(os.path.join(dataset_folder, 'test.csv'))
    X_test = test.drop("target", axis=1)
    y_test = test["target"].values.reshape(-1, 1)
    task.set_progress(20)
    
    task.upload_artifact(
        name='train_features',
        artifact_object=X_train
    )
    task.set_progress(30)
    
    # Обучаем модель
    task.connect(params.train_params)
    model = sklearn.ensemble.RandomForestClassifier(n_estimators=params.train_params.n_estimators)
    joblib.dump(model, "models/model.pkl", compress=True)
    model.fit(X_train, y_train)
    logger.info(f"Learn model {model}")
    task.set_progress(50)

    # Считаем метрики
    clearml_logger = task.get_logger()
    y_test_pred = model.predict_proba(X_test)[:, 1]
    y_test_pred_labels = model.predict(X_test)
    roc_auc = sklearn.metrics.roc_auc_score(y_test, y_test_pred)
    accuracy = sklearn.metrics.accuracy_score(y_test, y_test_pred_labels)
    clearml_logger.report_single_value("accuracy", accuracy)
    clearml_logger.report_single_value("ROC-AUC", accuracy)
    
    confusion_matrix = sklearn.metrics.confusion_matrix(y_test, y_test_pred_labels)
    clearml_logger.report_confusion_matrix("confusion_matrix", "ignored", matrix=confusion_matrix)


if __name__ == "__main__":
    app()
