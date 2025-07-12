from typing import Dict, List
from datetime import datetime, timezone
import pytz

from app.schemas.schemas import (
    ExtractRequest,
    Account,
    Summary,
    Transactions,
    Balance,
    Response,
)


class Normalizer:
    def normalize_data(
        self,
        account: Dict,
        balance: Dict,
        transactions: List,
    ):
        balance_pd = Balance(
            amount=balance.get("balance"), currency=balance.get("currency")
        )

        transactions_pd = []
        for transaction in transactions:
            transactions_pd.append(
                Transactions(
                    transaction_id=transaction.get("id"),
                    transaction_type=transaction.get("transaction_type"),
                    transaction_status=transaction.get("transaction_status"),
                    amount=transaction.get("transaction_amount"),
                    currency=balance.get("currency"),
                    direction=transaction.get("transaction_direction"),
                    description=transaction.get("transaction_description"),
                    date=transaction.get("transaction_date"),
                )
            )

        account_pd = Account(
            account_id=account.get("id"),
            account_type=account.get("account_type"),
            balance=balance_pd,
            transactions=transactions_pd,
        )

        return account_pd

    def create_response(
        self,
        data_source: ExtractRequest,
        total_transactions: int,
        duration: int,
        total_accounts: int,
        normalized_data: List,
    ):
        summary = Summary(
            total_accounts=total_accounts,
            total_transactions=total_transactions,
            processing_time_ms=duration,
            errors=[],
        )
        response = Response(
            user_document=data_source.user_document_number,
            extraction_date=self.__get_extraction_date(),
            accounts=normalized_data,
            summary=summary,
        )

        return response

    @staticmethod
    def __get_extraction_date():
        dt_utc = datetime.now(timezone.utc)

        tz_sao_paulo = pytz.timezone("America/Sao_Paulo")
        dt_sao_paulo = dt_utc.astimezone(tz_sao_paulo)

        return dt_sao_paulo.isoformat() + "Z"


normalizer = Normalizer()
