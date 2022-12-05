from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    profession: str


class DailyActivityBase(BaseModel):
    date: str
    workTime: int
    lostTime: int
    socialMediaUsage: int
    entertainmentTime: int
    targetObjectives: int
    completedObjectives: int
    score: float
    description: str
    user_id: int


class CompanyBase(BaseModel):
    name: str
    address: str


class ManagerBase(BaseModel):
    name: str
    address: str
    isSuper: bool
    company_id: int


class EmployeeBase(BaseModel):
    name: str
    address: str
    role: str
    department: str
    salary: int

# Creation Schemas


class UserCreate(UserBase):
    password: str


class DailyActivityCreate(DailyActivityBase):
    pass


class CompanyCreate(CompanyBase):
    pass


class ManagerCreate(ManagerBase):
    password: str


class EmployeeCreate(EmployeeBase):
    password: str


class DailyActivity(DailyActivityBase):
    id: int

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    daily_activities: list[DailyActivity] = []

    class Config:
        orm_mode = True


class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True


class Manager(ManagerBase):
    id: int
    company: Company

    class Config:
        orm_mode = True


class Employee(EmployeeBase):
    id: int
    daily_activities: list[DailyActivity] = []

    manager: Manager
    company: Company

    class Config:
        orm_mode = True
