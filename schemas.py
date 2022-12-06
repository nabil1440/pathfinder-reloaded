from pydantic import BaseModel


class DailyActivityBase(BaseModel):
    date: str
    workTime: int
    lostTime: int
    socialMediaUsage: int
    entertainmentTime: int
    targetObjectives: int
    completedObjectives: int
    description: str


class DailyActivityCreate(DailyActivityBase):
    pass


class DailyActivity(DailyActivityBase):
    id: int
    employee_id: int
    user_id: int
    score: float

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    profession: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class CompanyBase(BaseModel):
    name: str
    address: str


class CompanyCreate(BaseModel):
    name: str
    address: str
    manager_name: str
    manager_address: str
    password: str


class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True


class ManagerBase(BaseModel):
    name: str
    address: str


class ManagerCreate(ManagerBase):
    password: str
    company_id: int


class Manager(ManagerBase):
    id: int
    isSuper: bool
    company_id: int

    class Config:
        orm_mode = True


class EmployeeBase(BaseModel):
    name: str
    address: str
    role: str
    department: str
    salary: int


class EmployeeCreate(EmployeeBase):
    password: str


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


class LoginCred(BaseModel):
    name: str
    password: str


class UpdateEmployee(BaseModel):
    address: str
    role: str
    department: str
    salary: int


class UpdateManager(BaseModel):
    address: str
    isSuper: bool


class UpdateCompany(BaseModel):
    name: str
    address: str


class UpdateUser(BaseModel):
    profession: str
