from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class StudyScopeException(Exception):
    """This is the base class for all study-scope errors"""

    pass


class InvalidToken(StudyScopeException):
    """User has provided an invalid or expired token"""

    pass


class RevokedToken(StudyScopeException):
    """User has provided a token that has been revoked"""

    pass


class AccessTokenRequired(StudyScopeException):
    """User has provided a refresh token when an access token is needed"""

    pass


class RefreshTokenRequired(StudyScopeException):
    """User has provided an access token when a refresh token is needed"""

    pass


class UserAlreadyExists(StudyScopeException):
    """User has provided an email for a user who exists during sign up"""

    pass


class InvalidCredentials(StudyScopeException):
    """User has provided wrong email or password during log in"""

    pass


class InsufficientPermission(StudyScopeException):
    """User does not have the neccessary permissions to perform an action"""

    pass


class BookNotFound(StudyScopeException):
    """Book Not found"""

    pass


class TagNotFound(StudyScopeException):
    """Tag Not found"""

    pass


class TagAlreadyExists(StudyScopeException):
    """Tag already exists"""

    pass


class UserNotFound(StudyScopeException):
    """User Not found"""

    pass


class AccountNotVerified(Exception):
    """Account not yet verified"""

    pass


def createExceptionHandler(
    statusCode: int, initialDetail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exceptionHandler(request: Request, exc: StudyScopeException):

        return JSONResponse(content=initialDetail, statusCode=statusCode)

    return exceptionHandler


def registerAllErrors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        createExceptionHandler(
            statusCode=status.HTTP_403_FORBIDDEN,
            initialDetail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFound,
        createExceptionHandler(
            statusCode=status.HTTP_404_NOT_FOUND,
            initialDetail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )
    app.add_exception_handler(
        BookNotFound,
        createExceptionHandler(
            statusCode=status.HTTP_404_NOT_FOUND,
            initialDetail={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentials,
        createExceptionHandler(
            statusCode=status.HTTP_400_BAD_REQUEST,
            initialDetail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidToken,
        createExceptionHandler(
            statusCode=status.HTTP_401_UNAUTHORIZED,
            initialDetail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedToken,
        createExceptionHandler(
            statusCode=status.HTTP_401_UNAUTHORIZED,
            initialDetail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequired,
        createExceptionHandler(
            statusCode=status.HTTP_401_UNAUTHORIZED,
            initialDetail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenRequired,
        createExceptionHandler(
            statusCode=status.HTTP_403_FORBIDDEN,
            initialDetail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermission,
        createExceptionHandler(
            statusCode=status.HTTP_401_UNAUTHORIZED,
            initialDetail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
    app.add_exception_handler(
        TagNotFound,
        createExceptionHandler(
            statusCode=status.HTTP_404_NOT_FOUND,
            initialDetail={"message": "Tag Not Found", "error_code": "tag_not_found"},
        ),
    )

    app.add_exception_handler(
        TagAlreadyExists,
        createExceptionHandler(
            statusCode=status.HTTP_403_FORBIDDEN,
            initialDetail={
                "message": "Tag Already exists",
                "error_code": "tag_exists",
            },
        ),
    )

    app.add_exception_handler(
        BookNotFound,
        createExceptionHandler(
            statusCode=status.HTTP_404_NOT_FOUND,
            initialDetail={
                "message": "Book Not Found",
                "error_code": "book_not_found",
            },
        ),
    )

    app.add_exception_handler(
        AccountNotVerified,
        createExceptionHandler(
            statusCode=status.HTTP_403_FORBIDDEN,
            initialDetail={
                "message": "Account Not verified",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details",
            },
        ),
    )

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
