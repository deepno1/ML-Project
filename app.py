import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from src.mlproject.components.data_ingestion import dataIngestion
from src.mlproject.components.data_transformation import dataTransformation

if __name__ == '__main__':
    logging.info("The execution has started.")

    try:
        data_ingestion = dataIngestion()
        train_path, test_path = data_ingestion.init_ingestion()
        data_transformation = dataTransformation()
        data_transformation.data_transform(train_path,test_path)

    except Exception as e:
        raise CustomException(e,sys)
