import os
import sys
from dataclasses import dataclass

import numpy as np
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from firepred.exceptions import CustomException
from firepred.logger import logging
from firepred.utils import evaluate_models, save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = (
        os.path.abspath(os.path.join(os.path.dirname("__file__"), "."))
        + "/models/model.pkl"
    )


class ModelTrainer:
    def _init_(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array.iloc[:, :-1],
                train_array.iloc[:, -1],
                test_array.iloc[:, :-1],
                test_array.iloc[:, -1],
            )
            models = {
                "Random Forest": RandomForestClassifier(),
                "Naive Bayes": GaussianNB(),
                "Logistic Regression": LogisticRegression(),
                "SVC": SVC(),
                "LightGBM": LGBMClassifier(),
            }
            params = {
                "Naive Bayes": {"var_smoothing": np.logspace(0, -9, num=100)},
                "Random Forest": {
                    "max_features": ["sqrt", "log2", None],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Logistic Regression": {
                    "penalty": ["l1", "l2"],
                    "C": [0.01, 0.1, 1, 10, 100],
                },
                "LightGBM": {
                    "num_leaves": [8, 12, 16],
                    "min_child_samples": [5, 8, 10],
                },
                "SVC": {
                    "shrinking": [True, False],
                    "probability": [True, False],
                },
            }

            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params,
            )

            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            logging.info("best model is {best_model}")

            if best_model_score < 0.5:
                raise CustomException("No best model found")

            logging.info("Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            predicted = best_model.predict(X_test)

            accuracy = accuracy_score(y_test, predicted)
            return accuracy

        except Exception as e:
            raise CustomException(e, sys)
