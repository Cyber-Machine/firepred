import sys
import os
import pandas as pd
from src.exceptions import CustomException
from src.util import load_object


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = (
                os.path.abspath(os.path.join(os.path.dirname("__file__"), "."))
                + "/models/log_reg.pkl"
            )
            print(f"{model_path}")
            model = load_object(file_path=model_path)
            print("After Loading")
            preds = model.predict(features)
            print(f"{preds}")
            return preds

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(
        self,
        temperature: int,
        oxygen: int,
        humidity: int,
    ):
        self.temperature = temperature

        self.oxygen = oxygen

        self.humidity = humidity

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "temperature": [self.temperature],
                "oxygen": [self.oxygen],
                "humidity": [self.humidity],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
