from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import traceback

from ml.model import load_autoencoder_model
# from model import load_autoencoder_model


model = None
app = FastAPI()


class AutoencoderModelResponse(BaseModel):
    mse: float | str
    rmse: float | str
    error: str = "None error"


@app.on_event("startup")
async def startup_event():
    global model
    model = load_autoencoder_model()


@app.post("/predict/")
async def create_upload_json(request: Request):
    req_bytes = await request.body()
    json_str = req_bytes.decode('utf-8')
    try:
        dict_from_json: List[Dict[str, Any]] = json.loads(json_str)
    except Exception:
        return {"Error message": f"traceback - {traceback.format_exc()}",
                "json_str": request.body()}
    
    response_model = model(dict_from_json)

    response = AutoencoderModelResponse(
        mse=response_model.mse,
        rmse=response_model.rmse,
        error=response_model.error
    )

    return {"mse": response.mse,
            "rmse": response.rmse,
            "error": response.error}
