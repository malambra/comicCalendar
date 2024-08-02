from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.apache import HtpasswdFile

security = HTTPBasic()
htpasswd = HtpasswdFile('.htpasswd')

async def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if not htpasswd.check_password(credentials.username, credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username