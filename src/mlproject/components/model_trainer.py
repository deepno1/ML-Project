import os
import sys
from dataclasses import dataclass
from urllib.parse import urlparse
import numpy as np
from sklearn.metrics import mean_squared_error,mean_absolute_error
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from src.mlproject.utils import save_object,evaluate_models

@dataclass
class ModelTrainConfig:
    model_file_path : str = os.path.join('artifacts','model.pkl')

class ModelTrain:
    def __init__(self):
        self.modelTrainConfig = ModelTrainConfig()

    def init_model_training(self,train_arr,test_arr):
        try:
            logging.info("Split training and test input data")
            x_train_arr , y_train_arr = train_arr[:,:-1], train_arr[:,-1]
            x_test_arr , y_test_arr = test_arr[:,:-1], test_arr[:,-1]

            models = {
                    "Random Forest": RandomForestRegressor(),
                    "Decision Tree": DecisionTreeRegressor(),
                    "Gradient Boosting": GradientBoostingRegressor(),
                    "Linear Regression": LinearRegression(),
                    "XGBRegressor": XGBRegressor(),
                    "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                    "AdaBoost Regressor": AdaBoostRegressor(),
                }

            params={
                        "Decision Tree": {
                            'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                            'splitter':['best','random'],
                            'max_features':['sqrt','log2'],
                        },
                        "Random Forest":{
                            'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                            'max_features':['sqrt','log2',None],
                            'n_estimators': [8,16,32,64,128,256]
                        },
                        "Gradient Boosting":{
                            'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                            'learning_rate':[.1,.01,.05,.001],
                            'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                            'criterion':['squared_error', 'friedman_mse'],
                            'max_features': ['sqrt', 'log2', None],
                            'n_estimators': [8,16,32,64,128,256]
                        },
                        "Linear Regression":{},
                        "XGBRegressor":{
                            'learning_rate':[.1,.01,.05,.001],
                            'n_estimators': [8,16,32,64,128,256]
                        },
                        "CatBoosting Regressor":{
                            'depth': [6,8,10],
                            'learning_rate': [0.01, 0.05, 0.1],
                            'iterations': [30, 50, 100]
                        },
                        "AdaBoost Regressor":{
                            'learning_rate':[.1,.01,0.5,.001],
                            'loss':['linear','square','exponential'],
                            'n_estimators': [8,16,32,64,128,256]
                        }
                    }
            
            model_report,best_model = evaluate_models(x_train_arr,y_train_arr,x_test_arr,y_test_arr,models,params)
            logging.info('Receive models report and best model.')

            best_model_score = max(list(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(max(list(model_report.values())))]

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            
            logging.info(f"Best found model: {best_model_name} with score: {best_model_score}")

            save_object(self.modelTrainConfig.model_file_path,best_model)

            predicted = best_model.predict(x_test_arr)
            r2_square = r2_score(y_test_arr,predicted)

            return r2_square

        except Exception as e:
            raise CustomException(e,sys)
        