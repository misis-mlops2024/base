from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from loguru import logger
import time
import os

import mlflow
import pandas as pd
from typing import List


if 'AWS_ACCESS_KEY_ID' not in os.environ:
    logger.info("Hand made os environs")
    os.environ['AWS_ACCESS_KEY_ID'] = 'YCAJE7EasWFd2LlH_j9tbt1Ar'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'YCP5frOh73GPSCHB8_1OhKw7Nk259ak4wILSFhoF'
    os.environ['MLFLOW_TRACKING_URI'] = 'http://89.169.171.107:8000'
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'https://storage.yandexcloud.net/'


class InputResponse(BaseModel):
    data: List[List[float]]
    features: List[str]
    
class PredictResponse(BaseModel):
    output: float
    
    
def make_predict(data: InputResponse, model):
    data = pd.DataFrame(data.data, columns=data.features)
    pred = model.predict_proba(data)[:, 1]
    return PredictResponse(output=pred)


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    time.sleep(5)
    model = mlflow.sklearn.load_model(model_uri=f"models:/alexey-myshlyanov-model@prod")
    ml_models["model"] = model
    yield
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def main():
    return "Entry Point v5"


@app.get("/ready")
def ready() -> bool:
    return "model" in ml_models
    
        
@app.get("/predict/", response_model=PredictResponse)
def predict(request: InputResponse):
    return make_predict(request, ml_models['model'])
