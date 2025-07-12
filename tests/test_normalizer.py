from unittest.mock import patch

from tests.fixtures import (
    account_data,
    balance_data,
    transactions_data,
    normalized_data,
    extract_request,
    response_data,
)
from app.normalizers.normalizer import normalizer


def test_normalize_data(account_data, balance_data, transactions_data, normalized_data):
    response = normalizer.normalize_data(account_data, balance_data, transactions_data)
    assert response == normalized_data


@patch("app.normalizers.normalizer.Normalizer._Normalizer__get_extraction_date")
def test_create_response(
    mock_extraction_date, extract_request, normalized_data, response_data
):
    mock_extraction_date.return_value = "2025-07-12T18:59:06.594641-03:00Z"
    response = normalizer.create_response(extract_request, 2, 234, 1, [normalized_data])
    assert response == response_data
