import sys
import os
import pandas as pd
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from dataclasses import dataclass
from dotenv import load_dotenv
import pymysql
import pickle
import numpy as np


load_dotenv()
host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
db = os.getenv('db')

def read_sql_data():
    logging.info('Reading sql database started')
    try:
        mysql = pymysql.connect(
            host = host,
            user = user,
            password=password,
            db= db,
        )
        logging.info('Connetion Estabilish')

        df = pd.read_sql_query('select * from students',mysql)
        print()
        print(df.sample(5))

        return df

    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path,obj):
    try:
        dir = os.path.dirname(file_path)
        os.makedirs(dir,exist_ok=True)

        with open(file_path,'wb') as f:
            pickle.dump(obj,f)
            
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(x_train_arr,y_train_arr,x_test_arr,y_test_arr,models,params):
    try:
        logging.info('Start evaluating models')
        report = {}
        best_model = None
        best_params = None
        best_score = 0

        for i in range(len(list(models.keys()))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            gs = GridSearchCV(model,param,cv=3,error_score='raise')
            gs.fit(x_train_arr,y_train_arr)
            
            model.set_params(**gs.best_params_)
            model.fit(x_train_arr,y_train_arr)

            y_pred = model.predict(x_test_arr)
            test_score = r2_score(y_test_arr,y_pred)

            report[list(models.keys())[i]] = test_score

            if best_score < test_score:
                best_score = test_score
                best_model = model
                best_params = gs.best_params_

        return report,best_model,best_params


    except Exception as e:
        raise CustomException(e,sys)
    
    
