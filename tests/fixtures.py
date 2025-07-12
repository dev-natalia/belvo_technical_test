import pytest
from app.schemas.schemas import (
    Account,
    Balance,
    Transactions,
    ExtractRequest,
    Summary,
    Response,
)


@pytest.fixture
def valid_payload():
    return {
        "name": "Meu App",
        "organization_name": "Minha Organização",
        "organization_id": "org123",
        "user_document_number": "00011122233",
    }


@pytest.fixture
def extract_request():
    return ExtractRequest(
        name="Meu app",
        organization_name="Minha Organização",
        organization_id="org123",
        user_document_number="00011122233",
    )


@pytest.fixture
def account_data():
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "account_number": "123",
        "agency_number": "345",
        "bank_code": "567",
        "account_type": "checking",
        "consent_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }


@pytest.fixture
def balance_data():
    return {
        "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "balance": 100.50,
        "currency": "BRL",
        "calculated_at": "2025-07-12T21:37:42.905Z",
    }


@pytest.fixture
def transactions_data():
    return [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "transaction_type": "deposit",
            "transaction_date": "2025-07-12T21:38:42.272Z",
            "transaction_amount": 40.0,
            "transaction_description": "string",
            "transaction_status": "pending",
            "transaction_direction": "in",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f31232136",
            "account_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "transaction_type": "deposit",
            "transaction_date": "2025-07-13T21:38:42.272Z",
            "transaction_amount": 60.50,
            "transaction_description": "string",
            "transaction_status": "pending",
            "transaction_direction": "in",
        },
    ]


@pytest.fixture
def normalized_data():
    return Account(
        account_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        account_type="checking",
        balance=Balance(amount=100.5, currency="BRL"),
        transactions=[
            Transactions(
                transaction_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                transaction_type="deposit",
                transaction_status="pending",
                amount=40.0,
                currency="BRL",
                direction="in",
                description="string",
                date="2025-07-12T21:38:42.272Z",
            ),
            Transactions(
                transaction_id="3fa85f64-5717-4562-b3fc-2c963f31232136",
                transaction_type="deposit",
                transaction_status="pending",
                amount=60.5,
                currency="BRL",
                direction="in",
                description="string",
                date="2025-07-13T21:38:42.272Z",
            ),
        ],
    )


@pytest.fixture
def response_data():
    return Response(
        user_document="00011122233",
        extraction_date="2025-07-12T18:59:06.594641-03:00Z",
        accounts=[
            Account(
                account_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                account_type="checking",
                balance=Balance(amount=100.5, currency="BRL"),
                transactions=[
                    Transactions(
                        transaction_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        transaction_type="deposit",
                        transaction_status="pending",
                        amount=40.0,
                        currency="BRL",
                        direction="in",
                        description="string",
                        date="2025-07-12T21:38:42.272Z",
                    ),
                    Transactions(
                        transaction_id="3fa85f64-5717-4562-b3fc-2c963f31232136",
                        transaction_type="deposit",
                        transaction_status="pending",
                        amount=60.5,
                        currency="BRL",
                        direction="in",
                        description="string",
                        date="2025-07-13T21:38:42.272Z",
                    ),
                ],
            )
        ],
        summary=Summary(
            total_accounts=1, total_transactions=2, processing_time_ms=234, errors=[]
        ),
    )
