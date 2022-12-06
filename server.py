# Python commands to install the following modules
# fastapi uvicorn
# pip install fastapi
# pip install uvicorn
# How to run the project
# uvicorn server:app --reload

from typing import List
from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# Code related to database
import models
from database import SessionLocal, engine
# Auth code
from auth import AuthHandler
# Pydantic models for request and response body schemas
import schemas
# fore score calculation
from utils import calculate_score


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_handler = AuthHandler()
db = SessionLocal()


@app.get('/')
def home():
    return {'name': 'nabil'}


@app.post('/signup', response_model=schemas.User)
def userSignup(user: schemas.UserCreate):
    hashed_password = auth_handler.get_password_hash(user.password)
    db_user = models.User(
        name=user.name, password=hashed_password, profession=user.profession)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post('/signup/company')
def companySignup(credentials: schemas.CompanyCreate):
    hashed_password = auth_handler.get_password_hash(credentials.password)

    db_company = models.Company(
        name=credentials.name, address=credentials.address)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    db_manager = models.Manager(name=credentials.manager_name, address=credentials.manager_address,
                                password=hashed_password, company_id=db_company.id, isSuper=True)
    db.add(db_manager)
    db.commit()
    db.refresh(db_manager)

    return {'msg': f'Success! {db_company.name} created!'}


@app.post('/login')
def login(credentials: schemas.LoginCred):
    name = credentials.name
    password = credentials.password
    db_user = db.query(models.User).filter(models.User.name == name).first()

    if not db_user:
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')

    verified = auth_handler.verify_password(password, db_user.password)

    if verified:
        token = auth_handler.encode_token(db_user.id)
        return {'token': token}
    else:
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')


@app.post('/login/manager')
def loginManager(credentials: schemas.LoginCred):
    name = credentials.name
    password = credentials.password
    db_manager = db.query(models.Manager).filter(
        models.Manager.name == name).first()

    if not db_manager:
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')

    verified = auth_handler.verify_password(password, db_manager.password)

    if verified:
        token = auth_handler.encode_manager_token(
            db_manager.id, db_manager.company_id)
        return {'token': token}
    else:
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')


@app.post('/login/employee')
def loginEmployee(credentials: schemas.LoginCred):
    name = credentials.name
    password = credentials.password
    db_employee = db.query(models.Employee).filter(
        models.Employee.name == name).first()

    if not db_employee:
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')

    verified = auth_handler.verify_password(password, db_employee.password)

    if verified:
        token = auth_handler.encode_employee_token(
            db_employee.id, db_employee.company_id)
        return {'token': token}
    else:
        raise HTTPException(
            status_code=401, detail='Invalid username and/or password')


@app.get('/profile', response_model=schemas.User)
def getProfile(id=Depends(auth_handler.auth_wrapper)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


@app.patch('/profile')
def patchProfile(payload: schemas.UpdateUser, id=Depends(auth_handler.auth_wrapper)):
    return {'msg': 'Success!'}


@app.get('/profile/manager', response_model=schemas.Manager)
def getManagerProfile(payload=Depends(auth_handler.auth_wrapper_manager)):
    manager_id = payload['sub']
    company_id = payload['company_id']

    db_manager = db.query(models.Manager).filter(
        models.Manager.id == manager_id and models.Manager.company_id == company_id).first()

    return db_manager


@app.patch('/profile/manager')
def patchProfileManager():
    return {'msg': 'Success!'}


@app.get('/profile/employee', response_model=schemas.Employee)
def getEmployeeProfile(payload=Depends(auth_handler.auth_wrapper_employee)):
    employee_id = payload['sub']
    company_id = payload['company_id']

    db_employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id and models.Employee.company_id == company_id).first()

    return db_employee


@app.patch('/profile/employee')
def patchProfileEmployee():
    return {'msg': 'Success!'}


@app.post('/employees', response_model=schemas.Employee)
def createEmployee(employee: schemas.EmployeeCreate, creds=Depends(auth_handler.auth_wrapper_manager)):
    hashed_password = auth_handler.get_password_hash(employee.password)

    db_employee = models.Employee(name=employee.name, address=employee.address, role=employee.role,
                                  department=employee.department, salary=employee.salary, password=hashed_password, company_id=creds['company_id'], manager_id=creds['sub'])

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


@app.get('/employees', response_model=List[schemas.Employee])
def getEmployees(payload=Depends(auth_handler.auth_wrapper_manager)):
    company_id = payload['company_id']

    db_employees = db.query(models.Employee).filter(
        models.Employee.company_id == company_id).all()
    return db_employees


@app.get('/employees/{id}', response_model=schemas.Employee)
def getEmployeesId(payload=Depends(auth_handler.auth_wrapper_manager)):
    id = 1  # find out how to receive params into the function
    company_id = payload['company_id']

    db_employee = db.query(models.Employee).filter(
        models.Employee.company_id == company_id and models.Employee.id == id).first()

    return db_employee


@app.patch('/employees/{id}')
def updateEmployeesId():
    return {'msg': 'Success!'}


@app.delete('/employees/{id}')
def deleteEmployeesId():
    return {'msg': 'Success!'}


@app.post('/activities', response_model=schemas.DailyActivity)
def postActivity(payload: schemas.DailyActivityCreate, id=Depends(auth_handler.auth_wrapper)):

    derived_score = calculate_score(payload.workTime, payload.lostTime, payload.socialMediaUsage,
                                    payload.entertainmentTime, payload.targetObjectives, payload.completedObjectives)

    db_activity = models.DailyActivity(date=payload.date, workTime=payload.workTime, lostTime=payload.lostTime, socialMediaUsage=payload.socialMediaUsage, entertainmentTime=payload.entertainmentTime,
                                       targetObjectives=payload.targetObjectives, score=derived_score, completedObjectives=payload.completedObjectives, description=payload.description, user_id=id, employee_id=0)

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity


@app.get('/activities', response_model=List[schemas.DailyActivity])
def getActivities(id=Depends(auth_handler.auth_wrapper)):

    activities = db.query(models.DailyActivity).filter(
        models.DailyActivity.user_id == id).all()

    return activities


@app.get('/activities/{id}', response_model=schemas.DailyActivity)
def getActivity(id: int, user_id=Depends(auth_handler.auth_wrapper)):

    db_activity = db.query(models.DailyActivity).filter(
        models.DailyActivity.user_id == user_id and models.User.id == id).first()

    return db_activity


@app.post('/em-activities', response_model=schemas.DailyActivity)
def postActivity(payload: schemas.DailyActivityCreate, creds=Depends(auth_handler.auth_wrapper_employee)):

    derived_score = calculate_score(payload.workTime, payload.lostTime, payload.socialMediaUsage,
                                    payload.entertainmentTime, payload.targetObjectives, payload.completedObjectives)

    db_activity = models.DailyActivity(date=payload.date, workTime=payload.workTime, lostTime=payload.lostTime, socialMediaUsage=payload.socialMediaUsage, entertainmentTime=payload.entertainmentTime,
                                       targetObjectives=payload.targetObjectives, score=derived_score, completedObjectives=payload.completedObjectives, description=payload.description, user_id=0, employee_id=creds['sub'])

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    return db_activity


@app.get('/em-activities', response_model=List[schemas.DailyActivity])
def getActivities(creds=Depends(auth_handler.auth_wrapper_employee)):
    em_id = creds['sub']

    activities = db.query(models.DailyActivity).filter(
        models.DailyActivity.employee_id == em_id).all()

    return activities


@app.get('/em-activities/{id}', response_model=schemas.DailyActivity)
def getActivity(id: int, creds=Depends(auth_handler.auth_wrapper_employee)):
    em_id = creds['sub']

    db_activity = db.query(models.DailyActivity).filter(
        models.DailyActivity.employee_id == em_id and models.DailyActivity.id == id).first()

    return db_activity


@app.get('/employees/{id}/activities', response_model=List[schemas.DailyActivity])
def getEmployeeActivities(id: int, creds=Depends(auth_handler.auth_wrapper_manager)):

    db_activities = db.query(models.DailyActivity).filter(
        models.DailyActivity.employee_id == id).all()

    return db_activities


@app.get('/employees/{id}/activities/{a_id}', response_model=schemas.DailyActivity)
def getEmployeeActivities(id: int, a_id: int, creds=Depends(auth_handler.auth_wrapper_manager)):

    db_activity = db.query(models.DailyActivity).filter(
        models.DailyActivity.employee_id == id and models.DailyActivity.id == a_id).first()

    return db_activity


@app.patch('/activities/{id}')
def patchActivitiesId():
    return {'msg': 'Success!'}


@app.delete('/activities/{id}')
def deleteActivitiesId():
    return {'msg': 'Success!'}


@app.get('/company', response_model=schemas.Company)
def getCompaniesId(payload=Depends(auth_handler.auth_wrapper_manager)):

    company_id = payload['company_id']

    db_company = db.query(models.Company).filter(
        models.Company.id == company_id).first()
    return db_company


@app.get('/em-company', response_model=schemas.Company)
def getComapyAsEm(payload=Depends(auth_handler.auth_wrapper_employee)):
    company_id = payload['company_id']

    db_company = db.query(models.Company).filter(
        models.Company.id == company_id).first()
    return db_company


@app.patch('/company')
def patchCompaniesId():
    return {'msg': 'Success!'}
