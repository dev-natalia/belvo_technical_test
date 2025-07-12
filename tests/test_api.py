from tests.fixtures import valid_payload
from fastapi.testclient import TestClient
from fastapi import FastAPI
from unittest.mock import patch
from app.api.api import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


@patch("app.api.api.ExtractFinancialDataService.extract_data")
def test_extract_financial_data_returns_200(mock_extract_data, valid_payload):
    mock_extract_data.return_value = {
        "user_document": valid_payload["user_document_number"],
        "accounts": [],
        "summary": {
            "total_accounts": 0,
            "total_transactions": 0,
            "processing_time_ms": 1,
            "errors": [],
        },
        "extraction_date": "2025-07-12T13:02:06.320Z",
    }

    response = client.post("/extract-financial-data", json=valid_payload)

    assert response.status_code == 200
    body = response.json()
    assert body["user_document"] == valid_payload["user_document_number"]
    assert body["summary"]["total_accounts"] == 0

    mock_extract_data.assert_called_once()
