from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.exceptions import RequestValidationError
from requests.exceptions import Timeout

from app.schemas.schemas import ExtractRequest
from app.services.service import ExtractFinancialDataService
from app.core.error_handlers import (
    http_exception_handler,
    request_validation_error_handler,
    timeout_error_handler,
    generic_error_handler,
    value_error_handler,
)

router = APIRouter()
app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)
app.add_exception_handler(Timeout, timeout_error_handler)
app.add_exception_handler(Exception, generic_error_handler)
app.add_exception_handler(ValueError, value_error_handler)


@router.post("/extract-financial-data")
def extract_financial_data(payload: ExtractRequest):
    response = ExtractFinancialDataService(payload).extract_data()
    return response


app.include_router(router)
