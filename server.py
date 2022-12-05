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

# Write these routes:

# POST /login
@app.post('/login')
def getLogin():
    pass

# POST /login/manager
@app.post('/login/manager')
def postLoginManger():
    pass

# POST /login/employee
@app.post('/login/employee')
def postLoginManager():
    pass


# GET /profile
@app.get('/profile')
def getProfile():
    pass

# PATCH /profile
@app.patch('/profile')
def patchProfile():
    pass

# GET /profile/manager
@app.get('/profile/manager')
def getProfileManager():
    pass

# PATCH /profile/manager
@app.patch('/profile/manager')
def patchProfileManager():
    pass

# GET /profile/employee
@app.get('/profile/employee')
def getProfileEmployee():
    pass

# PATCH /profile/employee
@app.patch('/profile/employee')
def patchProfileEmployee():
    pass

# GET /employees
@app.get('/employees')
def getEmployees():
    pass

# GET /employees/{id}
@app.get('/employees/{id}')
def getEmployeesId():
    pass

# UPDATE /employees/{id}
@app.update('/employees/{id}')
def updateEmployeesId():
    pass

# DELETE /employees/{id}
@app.delete('/employees/{id}')
def deleteEmployeesId():
    pass

# POST /activities
@app.post('/activities')
def postActivities():
    pass

# GET /activities
@app.get('/activities')
def getActivities():
    pass

# GET /activities/{id}
@app.get('/activities/{id}')
def getActivitiesId():
    pass

# PATCH /activities/{id}
@app.patch('/activities/{id}')
def patchActivitiesId():
    pass

# DELETE /activities/{id}
@app.delete('/activities/{id}')
def deleteActivitiesId():
    pass

# GET /companies/{id}
@app.get('/companies/{id}')
def getCompaniesId():
    pass

# PATCH /companies/{id}
@app.patch('/companies/{id}')
def patchCompaniesId():
    pass

# =======================

# HTTP status code
# 2xx, 3xx, 4xx, 5xx
# 2xx: Okay
# 3xx: Redirect
# 4xx: There was an error from the client
# 5xx: There was an error on the server
