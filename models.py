from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, index=True)
    profession = Column(String)
    password = Column(String)


class DailyActivity(Base):
    __tablename__ = "daily_activities"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    date = Column(String)
    workTime = Column(Integer)
    lostTime = Column(Integer)
    socialMediaUsage = Column(Integer)
    entertainmentTime = Column(Integer)
    targetObjectives = Column(Integer)
    score = Column(Float)
    completedObjectives = Column(Integer)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    address = Column(String)


class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    address = Column(String)
    isSuper = Column(Boolean)
    password = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    address = Column(String)
    role = Column(String)
    department = Column(String)
    salary = Column(String)
    password = Column(String)

    company_id = Column(Integer, ForeignKey('companies.id'))
    manager_id = Column(Integer, ForeignKey('managers.id'))
