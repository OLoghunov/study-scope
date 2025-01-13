from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import jwt
import uuid
import logging

passwordContext = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600


def generatePasswordHash(password: str) -> str:
    hash = passwordContext.hash(password)
    return hash


def verifyPassword(password: str, hash: str) -> bool:
    return passwordContext.verify(password, hash)


def createAccessToken(userData: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}

    payload["user"] = userData
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )
    return token


def decodeToken(token: str) -> dict:
    try:
        tokenData = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return tokenData
    except Exception as e:
        logging.exception(e)
        return None
