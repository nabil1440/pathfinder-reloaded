from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, index=True)
    profession = Column(String)
    password = Column(String)

    acticity = relationship('Item', back_populates='user')


class DailyActivity(Base):
    __tablename__ = "daily_activities"

    date = Column(String, primary_key=True, unique=True)
    workTime = Column(Integer)
    lostTime = Column(Integer)
    socialMediaUsage = Column(Integer)
    entertainmentTime = Column(Integer)
    targetObjectives = Column(Integer)
    score = Column(Float)
    completedObjectives = Column(Integer)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))

    user = relationship("User", back_populates='daily_activities')
    employee = relationship('Employee', back_populates='daily_activities')


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    address = Column(String)

    manager = relationship('Manager', back_populates='company')
    employee = relationship('Employee', employees='company')


class Manager(Base):
    __tablename__ = 'managers'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    address = Column(String)
    isSuper = Column(Boolean)
    password = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship('Company', back_populates='managers')
    employee = relationship('Employee', employees='manager')


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

    manager = relationship('Manager', back_populates='employees')
    company = relationship('Company', back_populates='employees')
    daily_activity = relationship('DailyActivity', back_populates='employee')
