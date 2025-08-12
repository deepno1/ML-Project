import pickle
import sys
from src.mlproject.exception import CustomException
import asyncio
from concurrent.futures import ThreadPoolExecutor

def load_model():
    try:
        with open('D:/Python Projects/Projects/MLops-Project/artifacts/model.pkl','rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        raise CustomException(e,sys)

def preprocessing_obj():
    try:
        with open('D:/Python Projects/Projects/MLops-Project/artifacts/preprocessing.pkl','rb') as f:
            p_obj = pickle.load(f)
        return p_obj
    except Exception as e:
        raise CustomException(e,sys)
    
executor = ThreadPoolExecutor()

async def predict_async(model, processed_df):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, model.predict, processed_df)
    return result

async def predict_output(input_df):
    try:
        preprocessing = preprocessing_obj()
        model = load_model()

        processed_df = preprocessing.transform(input_df)

        predict_array = await predict_async(model, processed_df)
        predict = round(predict_array[0])

        if predict > 100:
            predict = 100
        elif predict < 0:
            predict = 0
        else:
            pass

        return predict
    
    except Exception as e:
        return CustomException(e,sys)