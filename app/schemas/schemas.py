from typing import Dict, List
from pydantic import BaseModel, PrivateAttr


class ExtractRequest(BaseModel):
    name: str
    organization_name: str
    organization_id: str
    user_document_number: str
    organization_type: str = "INDIVIDUAL"


class Balance(BaseModel):
    amount: float
    currency: str


class Transactions(BaseModel):
    transaction_id: str
    transaction_type: str
    transaction_status: str
    amount: float
    currency: str
    direction: str
    description: str
    date: str


class Summary(BaseModel):
    total_accounts: int
    total_transactions: int
    processing_time_ms: int
    errors: List


class Account(BaseModel):
    account_id: str
    account_type: str
    # account_status: str TODO: CHECAR VIA EMAIL QUE NÃO TEM ESSE CAMPO
    balance: Balance
    transactions: List[Transactions]


class Response(BaseModel):
    user_document: str
    extraction_date: str
    accounts: List[Account]
    summary: Summary
