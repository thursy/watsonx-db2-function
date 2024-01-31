import warnings
warnings.filterwarnings('ignore')

import io
import os
import ast
from fastapi import FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
import pandas as pd

from app.helpers.wxdb import *

app = FastAPI(
    title='Sample-app FastAPI and Docker',
    version = '1.0.0',
)


@app.get("/")
async def root():
    return {"message": "Hello World with GGF"}

@app.get("/ping")
async def ping():
    return "Hello, I am alive..."


@app.post("/wx_query")
async def get_recommendation(request: Request):

    try:
        user_input = await request.json()
        query = user_input['user_query']
        answer = await get_answer_wxdb(query)
        return answer
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))