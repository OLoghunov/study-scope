from src.auth.schemas import UserCreateModel

authPrefix = f"/api/0.1/auth"


def testUserCreation(fakeSession, fakeUserService, testClient):

    signupData = {
        "firstName": "Oleg",
        "lastName": "Logunov",
        "username": "oley03",
        "email": "loghunov1@gmail.com",
        "password": "qwerty12345",
    }

    response = testClient.post(
        url=f"{authPrefix}/signup",
        json=signupData,
    )

    userData = UserCreateModel(**signupData)

    assert fakeUserService.userExistsCalledOnce()
    assert fakeUserService.userExistsCalledOnceWith(signupData["email"], fakeSession)
    assert fakeUserService.createUserCalledOnce()
    assert fakeUserService.createUserCalledOnceWith(userData, fakeSession)
