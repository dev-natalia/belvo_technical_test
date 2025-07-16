from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from requests.exceptions import Timeout
from fastapi.exceptions import RequestValidationError


async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "Resource not found."},
        )
    elif exc.status_code == 422:
        return JSONResponse(
            status_code=422,
            content={
                "message": "Validation error when sending data to external API.",
                "detail": exc.detail,
            },
        )
    else:
        return JSONResponse(
            status_code=502,
            content={
                "message": "External service error. Please try again or contact support."
            },
        )


async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Validation error in request body.",
            "error": exc.body,
        },
    )


async def timeout_error_handler(request: Request, exc: Timeout):
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={"message": "Timeout: external API did not respond in time."},
    )


async def generic_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"message": "An unexpected error occurred. Please try again later."},
    )


async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        content={
            "message": "Internal configuration error.",
            "detail": str(exc),
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
