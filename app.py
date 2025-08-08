from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated,Literal
import pickle
import pandas as pd
import sys
from src.mlproject.exception import CustomException
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

def load_model():
    try:
        with open('artifacts/model.pkl','rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        raise CustomException(e,sys)

def preprocessing_obj():
    try:
        with open('artifacts/preprocessing.pkl','rb') as f:
            p_obj = pickle.load(f)
        return p_obj
    except Exception as e:
        raise CustomException(e,sys)
    

class InputConfig(BaseModel):

    gender: Annotated[Literal['male','female'],Field(...,description="Gender of student.")]
    race_ethnicity: Annotated[Literal['group B','group C','group A','group D','group E'],Field(...,description="Group of the student.")]
    parental_level_of_education: Annotated[Literal["bachelor's degree",'some college',"master's degree","associate's degree",'high school','some high school'],Field(...,description="Parents edu info.")]
    lunch: Annotated[Literal['standard','free/reduced'],Field(...,description="Lunch info of student.")]
    test_preparation_course: Annotated[Literal['none','completed'],Field(...,description="info about course complition of student.")]
    reading_score: Annotated[int,Field(...,gt=-1,lt=101,description="Student Reading Score.")]
    writing_score: Annotated[int,Field(...,gt=-1,lt=101,description="Student writing Score.")]

@app.get('/')
async def root():
    return 'Frontend'

@app.get('/about')
async def about():
    return 'Frontend about section'

executor = ThreadPoolExecutor()

async def predict_async(model, processed_df):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, model.predict, processed_df)
    return result

@app.post('/predict')
async def prediction(input : InputConfig):
    try:
        input = input.model_dump()
        input_df = pd.DataFrame([input])

        preprocessing = preprocessing_obj() 
        model = load_model()

        processed_df = preprocessing.transform(input_df)
        # Run prediction asynchronously in thread pool
        predict_array = await predict_async(model, processed_df)
        predict = round(predict_array[0])

        if predict > 100:
            predict = 100
        elif predict < 0:
            predict = 0
        else:
            pass

        return JSONResponse(status_code=200 , content = {'math_score' : predict})
    except Exception as e:
        raise HTTPException(status_code=400 , detail = str(e))
