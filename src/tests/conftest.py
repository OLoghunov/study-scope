from src.db.main import getSession
from src.auth.dependencies import RoleChecker, AccessTokenBearer, RefreshTokenBearer
from src import app
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient


mockSession = Mock()
mockUserService = Mock()
mockBookService = Mock()


def getMockSession():
    yield mockSession


accessTokenBearer = AccessTokenBearer()
refreshTokenBearer = RefreshTokenBearer()
roleChecker = RoleChecker(["admin"])

app.dependency_overrides[getSession] = getMockSession
app.dependency_overrides[roleChecker] = Mock()
app.dependency_overrides[refreshTokenBearer] = Mock()


@pytest.fixture
def fakeSession():
    return mockSession


@pytest.fixture
def fakeUserService():
    return mockUserService


@pytest.fixture
def testClient():
    return TestClient(app)


@pytest.fixture
def fakeBookService():
    return mockBookService
