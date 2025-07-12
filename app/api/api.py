from fastapi import APIRouter
from app.schemas.schemas import ExtractRequest
from app.services.service import ExtractFinancialDataService

router = APIRouter()


@router.post("/extract-financial-data")
def extract_financial_data(payload: ExtractRequest):
    """
    Endpoint to extract financial data from the provided payload.

    Args:
        payload (ExtractRequest): The request payload containing financial data.

    Returns:
        dict: A dictionary containing the extracted financial data.
    """
    response = ExtractFinancialDataService(payload).extract_data()
    return {"message": "Financial data extraction is not implemented yet."}
