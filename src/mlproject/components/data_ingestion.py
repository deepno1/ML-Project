import sys
import os
import pandas as pd
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from dataclasses import dataclass
from src.mlproject.utils import read_sql_data
from sklearn.model_selection import train_test_split

@dataclass
class dataIngestionConfig:
    train_data_path : str = os.path.join('artifacts','train.csv')
    test_data_path : str = os.path.join('artifacts','test.csv')
    raw_data_path : str = os.path.join('artifacts','raw.csv')

class dataIngestion:
    def __init__(self):
        self.ingestionConfig = dataIngestionConfig()

    def init_ingestion(self):
        try:
            raw_data = read_sql_data()

            logging.info("Reading completed Mysql Database")

            os.makedirs(os.path.dirname(self.ingestionConfig.train_data_path),exist_ok=True)

            raw_data.to_csv(self.ingestionConfig.raw_data_path,index=False,header=True)

            train_data,test_data = train_test_split(raw_data,test_size=0.2,random_state=32)
            train_data.to_csv(self.ingestionConfig.train_data_path,index=False,header=True)
            test_data.to_csv(self.ingestionConfig.test_data_path,index=False,header=True)

            logging.info('Data Ingestion is compeleted')

            return (
                self.ingestionConfig.train_data_path,
                self.ingestionConfig.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

