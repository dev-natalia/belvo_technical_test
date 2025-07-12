from app.core.retry_utils import request_with_retry

BASE_URL = "http://localhost:8000"


class Consents:
    def create_consent(self, user_document_number: str, token: str):
        headers = {"Authorization": f"{token}"}
        payload = {"document_number": user_document_number}

        response = request_with_retry(
            "POST", f"{BASE_URL}/consent/", headers=headers, json=payload
        )

        consent = response.json()
        if consent["status"] != "APPROVED":
            raise Exception("Consent not approved")

        return consent.get("token"), consent.get("id")

    def get_consent(self, user_document_number: str, token: str):
        headers = {"Authorization": f"{token}"}
        response = request_with_retry("GET", f"{BASE_URL}/consent/", headers=headers)

        consents = response.json()
        for consent in consents:
            if consent.get("document_number") == user_document_number:
                if consent.get("status") != "APPROVED":
                    raise Exception("Consent not approved")
                return consent.get("token"), consent.get("id")

        return None, None


consents = Consents()
