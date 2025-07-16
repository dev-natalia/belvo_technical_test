import time

from app.core.encrypted_cache import cache
from app.clients.clients import clients
from app.clients.consents import consents
from app.extractors.extractor import extractor
from app.normalizers.normalizer import normalizer
from app.schemas.schemas import ExtractRequest


class ExtractFinancialDataService:
    def __init__(self, data_source: ExtractRequest):
        self.data_source = data_source

    def extract_data(self):
        start_time = time.time()

        dynamic_token = self.__get_dynamic_client_token()
        consent_token, consent_id = self.__get_consent_token(dynamic_token)
        accounts_raw = extractor.get_account(consent_token, consent_id)

        total_transactions = 0
        normalized_data = []

        for account in accounts_raw:
            account_id = account.get("id")
            balance = extractor.get_account_balance(consent_token, account_id)
            transactions = extractor.get_account_transactions(consent_token, account_id)
            total_transactions += len(transactions)

            normalized_data.append(
                normalizer.normalize_data(account, balance, transactions)
            )

        duration_ms = int((time.time() - start_time) * 1000)

        response = normalizer.create_response(
            self.data_source,
            total_transactions,
            duration_ms,
            len(accounts_raw),
            normalized_data,
        )

        return response

    def __get_dynamic_client_token(self) -> str:
        org_id = self.data_source.organization_id
        dynamic_token = cache.get_dynamic_client_token(org_id)

        if dynamic_token:
            return dynamic_token

        dynamic_token = clients.get_dynamic_client_token(org_id)

        if not dynamic_token:
            dynamic_token = clients.create_dynamic_client_token(self.data_source)

        cache.set_dynamic_client_token(org_id, dynamic_token)
        return dynamic_token

    def __get_consent_token(self, dynamic_token: str) -> str:
        document = self.data_source.user_document_number
        consent_token, consent_id = cache.get_consent(document)

        if consent_token:
            return consent_token, consent_id

        consent_token, consent_id = consents.get_consent(document, dynamic_token)

        if not consent_token:
            consent_token, consent_id = consents.create_consent(document, dynamic_token)

        cache.set_consent(document, consent_token, consent_id)
        return consent_token, consent_id
