# Python commands to install the following modules
# fastapi uvicorn
# pip install fastapi
# pip install uvicorn
# How to run the project
# uvicorn server:app --reload

from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
# Code related to database
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def home():
    return {'name': 'nabil'}


titans = ['Tim Dodd', 'Dick Grayson']


@app.get('/titans')
def getProducts():
    return titans


@app.get('/titans/{id}')
def getOneProduct(id: int):
    if (id > len(titans) - 1):
        return 'Out of range!'

    return titans[id]

# HTTP status code
# 2xx, 3xx, 4xx, 5xx
# 2xx: Okay
# 3xx: Redirect
# 4xx: There was an error from the client
# 5xx: There was an error on the server
