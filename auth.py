import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
# DB query stuff
from database import SessionLocal
import models


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=30, minutes=0),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'company_id': None,
            'type': 'user'
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def encode_manager_token(self, manager_id, company_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=30, minutes=0),
            'iat': datetime.utcnow(),
            'sub': manager_id,
            'company_id': company_id,
            'type': 'manager'
        }

        # need to query database here
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def encode_employee_token(self, employee_id, company_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=30, minutes=0),
            'iat': datetime.utcnow(),
            'sub': employee_id,
            'company_id': company_id,
            'type': 'employee'
        }

        # need to query database here
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_manager_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])

            if payload['type'] != 'manager':
                raise HTTPException(
                    status_code=401, detail='Invalid token!')

            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def decode_employee_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])

            if payload['type'] != 'employee':
                raise HTTPException(
                    status_code=401, detail='Invalid token!')

            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])

            if payload['type'] != 'user':
                raise HTTPException(
                    status_code=401, detail='Invalid token!')

            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def auth_wrapper_manager(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_manager_token(auth.credentials)

    def auth_wrapper_employee(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_employee_token(auth.credentials)
