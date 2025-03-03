import jwt
import globals
import datetime
from helper import formatted_response
from app.config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()

def create_jwt_token(user_id: str):
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=30)
    payload = {"sub": user_id, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail=globals.TOKEN_EXPIRED)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail=globals.INVALID_TOKEN)


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return verify_jwt_token(credentials.credentials)
