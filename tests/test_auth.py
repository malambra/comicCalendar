# tests/test_auth.py
import os
from datetime import datetime, timedelta
from app.auth.auth import authenticate_user, create_access_token
from passlib.apache import HtpasswdFile
from jose import jwt

def test_authenticate_user_valid():
    htpasswd = HtpasswdFile(".htpasswd")
    htpasswd.set_password("admin", "password")
    htpasswd.save()

    user = authenticate_user("admin", "password")
    assert user is not None
    assert user.username == "admin"

def test_authenticate_user_invalid():
    user = authenticate_user("invaliduser", "invalidpassword")
    assert user is None

def test_create_access_token():
    data = {"sub": "admin"}  # Cambiado de "test" a "admin"
    token = create_access_token(data)
    assert token is not None

    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    assert decoded_token["sub"] == "admin"
    assert "exp" in decoded_token

def test_create_access_token_with_expiration():
    data = {"sub": "admin"}
    expires_delta = timedelta(minutes=5)
    token = create_access_token(data, expires_delta=expires_delta)
    assert token is not None

    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    assert decoded_token["sub"] == "admin"
    assert "exp" in decoded_token

    expire_time = datetime.utcfromtimestamp(decoded_token["exp"])
    expected_expire_time = datetime.utcnow() + expires_delta
    assert abs((expire_time - expected_expire_time).total_seconds()) < 1

def test_create_access_token_default_expiration():
    data = {"sub": "admin"}
    token = create_access_token(data)
    assert token is not None

    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    assert decoded_token["sub"] == "admin"
    assert "exp" in decoded_token

    expire_time = datetime.utcfromtimestamp(decoded_token["exp"])
    expected_expire_time = datetime.utcnow() + timedelta(minutes=15)
    assert abs((expire_time - expected_expire_time).total_seconds()) < 1

def test_create_access_token_custom_expiration():
    data = {"sub": "admin"}
    expires_delta = timedelta(minutes=30)
    token = create_access_token(data, expires_delta=expires_delta)
    assert token is not None

    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    assert decoded_token["sub"] == "admin"
    assert "exp" in decoded_token

    expire_time = datetime.utcfromtimestamp(decoded_token["exp"])
    expected_expire_time = datetime.utcnow() + expires_delta
    assert abs((expire_time - expected_expire_time).total_seconds()) < 1

def test_create_access_token_with_additional_data():
    data = {"sub": "admin", "role": "admin"}
    token = create_access_token(data)
    assert token is not None

    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    assert decoded_token["sub"] == "admin"
    assert decoded_token["role"] == "admin"
    assert "exp" in decoded_token