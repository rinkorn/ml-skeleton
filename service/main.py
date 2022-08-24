"""FastAPI Titanic model inference example"""

from typing import Optional
import os

import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
# from starlette_exporter import PrometheusMiddleware, handle_metrics
from pydantic import BaseModel
from sklearn.pipeline import Pipeline

from titanic.models.serialize import load

app = FastAPI()
# app.add_middleware(PrometheusMiddleware)
# app.add_route("/metrics", handle_metrics)

MODEL = os.getenv("MODEL", default="baseline.v1")


class Model:
    pipeline: Optional[Pipeline] = None


class Passanger(BaseModel):
    Pclass: int
    Name: str
    Sex: str
    Age: Optional[int] = None
    SibSp: int
    Parch: int
    Ticket: str
    Fare: float
    Cabin: Optional[str] = None
    Embarked: Optional[str] = None


@app.on_event("startup")
def load_model():
    # Model.pipeline = load(MODEL)
    pass


@app.get("/")
def read_healthcheck():
    return {"status": "Green", "version": "0.1.2"}


@app.post("/predict")
def predict(passenger_id: int, passanger: Passanger):
    df = pd.DataFrame([passanger.dict()])
    df.fillna(value=np.nan, inplace=True, downcast=False)
    if Model.pipeline is None:
        raise HTTPException(status_code=503, detail="No model loaded")
    try:
        pred = int(Model.pipeline.predict(df)[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"passenger_id": passenger_id, "survived": pred}
