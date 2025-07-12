from fastapi import FastAPI, APIRouter
from app.schemas.schemas import ExtractRequest
from app.services.service import ExtractFinancialDataService

router = APIRouter()


@router.post("/extract-financial-data")
def extract_financial_data(payload: ExtractRequest):
    response = ExtractFinancialDataService(payload).extract_data()
    return response


app = FastAPI()
app.include_router(router)
