from unittest.mock import patch
from app.services.service import ExtractFinancialDataService
from tests.fixtures import extract_request, response_data, normalized_data


@patch("app.normalizers.normalizer.Normalizer.create_response")
@patch("app.normalizers.normalizer.Normalizer.normalize_data")
@patch("app.extractors.extractor.Extractor.get_account_transactions")
@patch("app.extractors.extractor.Extractor.get_account_balance")
@patch("app.extractors.extractor.Extractor.get_account")
@patch("app.clients.consents.Consents.get_consent")
@patch("app.clients.clients.Clients.get_dynamic_client_token")
@patch("app.core.cache.Cache.get_consent")
@patch("app.core.cache.Cache.get_dynamic_client_token")
def test_extract_data_full_flow(
    mock_get_dynamic_cache,
    mock_get_consent_cache,
    mock_get_dynamic_token,
    mock_get_consent,
    mock_get_account,
    mock_get_balance,
    mock_get_transactions,
    mock_normalize_data,
    mock_create_response,
    extract_request,
    response_data,
    normalized_data,
):
    mock_get_dynamic_cache.return_value = None
    mock_get_consent_cache.return_value = (None, None)

    mock_get_dynamic_token.return_value = "dynamic-token"
    mock_get_consent.return_value = ("consent-token", "consent-id")

    mock_get_account.return_value = [{"id": "acc1"}]
    mock_get_balance.return_value = {"amount": 100.0, "currency": "BRL"}
    mock_get_transactions.return_value = [
        {
            "id": "tx1",
            "transaction_type": "deposit",
            "transaction_status": "completed",
            "transaction_amount": 100.0,
            "transaction_direction": "in",
            "transaction_description": "Salário",
            "transaction_date": "2025-07-12T12:00:00Z",
        }
    ]

    mock_normalize_data.return_value = normalized_data
    mock_create_response.return_value = response_data

    service = ExtractFinancialDataService(extract_request)
    result = service.extract_data()

    assert result == response_data
