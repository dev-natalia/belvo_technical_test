from app.core.retry_utils import request_with_retry


BASE_URL = "http://localhost:8000"


class Extractor:
    def get_account(self, consent_token: str, consent_id: str):
        page_number = 1
        next_page = True
        matched_accounts = []

        headers = {"Authorization": f"{consent_token}"}

        while next_page == True:
            params = {"page": page_number}
            response = request_with_retry(
                "GET", f"{BASE_URL}/account/", headers=headers, params=params
            )

            response_dict = response.json()

            accounts = response_dict.get("items")

            for account in accounts:
                if account.get("consent_id") == consent_id:
                    matched_accounts.append(account)

            next_page = response_dict.get("has_next")
            page_number += 1

        if len(matched_accounts) == 0:
            raise Exception("Account not found")

        return matched_accounts

    def get_account_balance(self, consent_token: str, account_id: str):
        headers = {"Authorization": f"{consent_token}"}
        response = request_with_retry(
            "GET", f"{BASE_URL}/account/{account_id}/balance/", headers=headers
        )

        return response.json()

    def get_account_transactions(self, consent_token: str, account_id: str):
        next_page = True
        page_number = 1
        transactions = []

        headers = {"Authorization": f"{consent_token}"}

        while next_page == True:
            params = {"page": page_number}
            response = request_with_retry(
                "GET",
                f"{BASE_URL}/account/{account_id}/transactions/",
                headers=headers,
                params=params,
            )

            response_dict = response.json()
            transactions.extend(response_dict.get("items"))

            next_page = response_dict.get("has_next")
            page_number += 1

        return transactions


extractor = Extractor()
