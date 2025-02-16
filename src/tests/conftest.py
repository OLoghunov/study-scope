from src.db.main import getSession
from src import app
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient


mockSession = Mock()
mockUserService = Mock()

def getMockSession():
    yield mockSession
    
app.dependency_overrides[getSession] = getMockSession

@pytest.fixture
def fakeSession():
    return mockSession

@pytest.fixture
def fakeUserService():
    return mockUserService

@pytest.fixture
def testClient():
    return TestClient(app)