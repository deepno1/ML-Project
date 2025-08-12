from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated,Literal
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from src.mlproject.pipelines.Prediction_pipeline import predict_output

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {'Message':'Students Maths Marks Prediction API'}

@app.get('/health')
def health_check():
    return {'Status':'OK'}

@app.get('/about')
async def about():
    return 'Students Maths Marks Prediction'

@app.post('/predict')
async def prediction(input: InputConfig):
    try:

        input_dict = input.model_dump()
        input_df = pd.DataFrame([input_dict])

        predict = await predict_output(input_df)

        return JSONResponse(status_code=200, content={'math_score': predict})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

