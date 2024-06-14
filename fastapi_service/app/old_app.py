from fastapi import FastAPI, UploadFile, Request, Body, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pathlib import Path
from typing import List, Dict, Any
import base64
import json
import traceback


from model import load_autoencoder_model

model = None
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)


class AutoencoderModelResponse(BaseModel):
    mse: float | str
    rmse: float | str
    error: str = "None error"


# class JsonTyping():



@app.on_event("startup")
def startup_event():
    global model
    model = load_autoencoder_model()


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict/")
# def create_upload_json(json_text: Any = Body(None)):
# async def create_upload_json(json_text = Body(...)):
async def create_upload_json(json_text: str = Form(...)):
    # dec_payload = json_text.decode('utf-8')
    try:
        # payload
        # json_bytes = upload.file.read()
        # dec_payload = json_text.decode('utf-8')
        dict_from_json: List[Dict[str, Any]] = json.loads(json_text)
        # dict_from_json: List[Dict[str, Any]] = upload
    except Exception:
        return {"message": f"traceback - {traceback.format_exc()}",
                "dec_payload": json_text}
    
    # return dict_from_json
    
    response_model = model(dict_from_json)

    response = AutoencoderModelResponse(
        mse=response_model.mse,
        rmse=response_model.rmse,
        error=response_model.error
    )

    # return templates.TemplateResponse("display.html",
    #                                   {"request": request,
    #                                    "mse": response.mse,
    #                                    "rmse": response.rmse})
    return {"mse": response.mse,
            "rmse": response.rmse,
            "error": response.error}


# @app.post("/upload_json/")
# def create_upload_json(request: Request, file_upload: UploadFile):
#     try:
#         json_bytes = file_upload.file.read()
#         dict_from_json = json.loads(json_bytes.decode('utf-8'))
#         with open("uploaded_" + file_upload.filename, "wb") as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file_upload.file.close()

#     base64_encoded_image = base64.b64encode(contents).decode("utf-8")

#     return templates.TemplateResponse("display.html", {"request": request,  "myImage": base64_encoded_image})
