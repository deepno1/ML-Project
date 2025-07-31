import sys
import os
import pandas as pd
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from dataclasses import dataclass
from dotenv import load_dotenv
import pymysql


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