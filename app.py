import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from src.mlproject.components.data_ingestion import dataIngestion
from src.mlproject.components.data_transformation import dataTransformation
from src.mlproject.components.model_trainer import ModelTrain

if __name__ == '__main__':
    logging.info("The execution has started.")

    try:
        # data ingestion
        data_ingestion = dataIngestion()
        train_path, test_path = data_ingestion.init_ingestion()

        # data transformation
        data_transformation = dataTransformation()
        transformed_train_df,transformed_test_df,file_path = data_transformation.data_transform(train_path,test_path)

        # model training
        model_train = ModelTrain()
        r2_square = model_train.init_model_training(transformed_train_df,transformed_test_df)
        print(r2_square)

    except Exception as e:
        raise CustomException(e,sys)
