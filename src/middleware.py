import time
import logging

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger("uvicorn.access")
logger.disabled = True


def registerMiddleware(app: FastAPI):

    @app.middleware("http")
    async def customLogging(request: Request, callNext):
        startTime = time.time()

        response = await callNext(request)
        processingTime = time.time() - startTime

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} - completed after {processingTime} s"
        print(message)

        return response
