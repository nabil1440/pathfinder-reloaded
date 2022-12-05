from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# CRUD functions
# USER-G1U, DAILYACT-GG1UD, COMPANY-G1U, MANAGER-G1U, Employee-GG1U


def getUserProfile(db: Session):
    pass


def updateProfile(db: Session):
    pass


def getDays(db: Session):
    pass


def getOneDay(db: Session):
    pass


def getCompany(db: Session):
    pass


def updateCompany(db: Session):
    pass


def getManager(db: Session):
    pass


def updateManager(db: Session):
    pass


def getEmployees(db: Session):
    pass


def getOneEmployee(db: Session):
    pass


def updateEmployee(db: Session):
    pass
