from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
from loguru import logger
import time
import os

import mlflow
import pandas as pd
from typing import List


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


@app.get("/metrics")
def metrics():
    
    
        
@app.get("/predict/", response_model=PredictResponse)
def predict(request: InputResponse):
    return make_predict(request, ml_models['model'])
