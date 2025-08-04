import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.mlproject.utils import save_object

from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
import os

@dataclass
class dataTransformationConfig:
    preprocessing_obj_file_path : str = os.path.join('artifacts','preprocessing.pkl')

class dataTransformation:
    def __init__(self):
        self.data_transform_config = dataTransformationConfig()

    def get_data_transform_obj(self):

        cat_col = ['gender',
                    'race_ethnicity',
                    'parental_level_of_education',
                    'lunch',
                    'test_preparation_course']
        num_col = ['reading_score', 'writing_score']

        num_custom_transformer = Pipeline([
            ('imputer',SimpleImputer(strategy='median')),
            ('scale',StandardScaler())
        ])

        cat_custom_transformer = Pipeline([
            ('imputer',SimpleImputer(strategy='most_frequent')),
            ('one-hot',OneHotEncoder())
        ])

        logging.info(f"Categorical Columns:{cat_col}")
        logging.info(f"Numerical Columns:{num_col}")

        preprocessor = ColumnTransformer([
            ('cat_col_trans',cat_custom_transformer,cat_col),
            ('num_col_trans',num_custom_transformer,num_col)
        ])

        return preprocessor
    
    def data_transform(self,train_path,test_path):

        try :
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading the train and test file")

            indi_x_train = train_df.drop(columns=['math_score'],axis=1)
            dep_y_train = train_df['math_score']
            indi_x_test = test_df.drop(columns=['math_score'],axis=1)
            dep_y_test = test_df['math_score']

            logging.info("Applying Preprocessing on training and test dataframe")

            transformer = self.get_data_transform_obj()
            transformed_indi_x_train = transformer.fit_transform(indi_x_train)
            transformed_indi_x_test = transformer.transform(indi_x_test)

            save_object(self.data_transform_config.preprocessing_obj_file_path,transformer)
            logging.info("Saved preprocessing object")

            transformed_train_df = np.c_[transformed_indi_x_train, np.array(dep_y_train)]
            transformed_test_df = np.c_[transformed_indi_x_test, np.array(dep_y_test)]

            return(
                transformed_train_df,
                transformed_test_df,
                self.data_transform_config.preprocessing_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)