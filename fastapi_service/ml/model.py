import traceback
import logging
import traceback
import os
from dataclasses import dataclass
from typing import List, Dict, Any

from train.train import Autoencoder_Model
from prepData.prepData import PrepData
from dotenv import load_dotenv

load_dotenv()

USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
TOKEN = os.environ.get('TOKEN')
URI = os.environ.get('URI')
NAME_MODEL = os.environ.get('NAME_MODEL')
VERSION_MODEL = os.environ.get('VERSION_MODEL')


@dataclass
class AutoencoderModelPrediction:
    """Class representing a sentiment prediction result."""

    mse: float | str = "None value"
    rmse: float | str = "None value"
    error: str = "No Error"


def load_autoencoder_model():
    """Load a pre-trained sentiment analysis model.

    Returns:
        model (function): A function that takes a text input and returns a SentimentPrediction object.
    """
    try:
        model_class = Autoencoder_Model()
        logging.info(f"Success get MODEL CLASS")
    except Exception:
        logging.error(f"Get MODEL CLASS error - {traceback.format_exc()}")
        raise
    try:
        logging.info(f"Waiting get model ...")
        model_hf = model_class.load_model_from_MlFlow(dagshub_toc_username=USER, dagshub_toc_pass=TOKEN, dagshub_toc_tocen=TOKEN)
        logging.info(f"Success get MODEL")
    except Exception:
        logging.error(f"Get MODEL error - {traceback.format_exc()}")
        raise

    def model(data_dict: List[Dict[str, Any]]) -> AutoencoderModelPrediction:

        prep_class = PrepData()

        try:
            numpy_from_data = prep_class.json_to_numpy(data_dict)
            predict_data = model_class.start_predict_model(model_hf, numpy_from_data)
        except Exception:
            return AutoencoderModelPrediction(
                error=f"ERROR: data_dict ({data_dict}) caused an error - {traceback.format_exc()}"
            )
        

        mse_rmse_res: Dict[str, Any] = model_class.start_active_validate(predict_data, numpy_from_data)

        return AutoencoderModelPrediction(
            mse=mse_rmse_res['MSE'],
            rmse=mse_rmse_res['RMSE'],
        )

    return model
