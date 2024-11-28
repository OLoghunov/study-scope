from passlib.context import CryptContext


passwordContext = CryptContext(schemes=["bcrypt"])


def generatePasswordHash(password: str) -> str:
    hash = passwordContext.hash(password)

    return hash


def verifyPassword(password: str, hash: str) -> bool:
    return passwordContext.verify(password, hash)
