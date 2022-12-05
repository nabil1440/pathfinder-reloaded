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


@app.post('/signup')
def userSignup():
    pass


@app.post('/signup/company')
def companySignup():
    pass


@app.post('/login')
def getLogin():
    pass


@app.post('/login/manager')
def postLoginManger():
    pass


@app.post('/login/employee')
def postLoginManager():
    pass


@app.get('/profile')
def getProfile():
    pass


@app.patch('/profile')
def patchProfile():
    pass


@app.get('/profile/manager')
def getProfileManager():
    pass


@app.patch('/profile/manager')
def patchProfileManager():
    pass


@app.get('/profile/employee')
def getProfileEmployee():
    pass


@app.patch('/profile/employee')
def patchProfileEmployee():
    pass


@app.get('/employees')
def getEmployees():
    pass


@app.get('/employees/{id}')
def getEmployeesId():
    pass


@app.patch('/employees/{id}')
def updateEmployeesId():
    pass


@app.delete('/employees/{id}')
def deleteEmployeesId():
    pass


@app.post('/activities')
def postActivities():
    pass


@app.get('/activities')
def getActivities():
    pass


@app.get('/activities/{id}')
def getActivitiesId():
    pass


@app.patch('/activities/{id}')
def patchActivitiesId():
    pass


@app.delete('/activities/{id}')
def deleteActivitiesId():
    pass


@app.get('/companies/{id}')
def getCompaniesId():
    pass


@app.patch('/companies/{id}')
def patchCompaniesId():
    pass


# HTTP status code
# 2xx, 3xx, 4xx, 5xx
# 2xx: Okay
# 3xx: Redirect
# 4xx: There was an error from the client
# 5xx: There was an error on the server
