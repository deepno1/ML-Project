import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from src.mlproject.components.data_ingestion import dataIngestion

if __name__ == '__main__':
    logging.info("The execution has started.")

    try:
        data_ingestion = dataIngestion()
        data_ingestion.init_ingestion()

    except Exception as e:
        raise CustomException(e,sys)
