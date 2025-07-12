from app.core.retry_utils import request_with_retry
from app.schemas.schemas import ExtractRequest

BASE_URL = "http://localhost:8000"


class Clients:
    def create_dynamic_client_token(self, data_source: ExtractRequest):
        payload = data_source.export_with_private()
        payload.pop("user_document_number")

        response = request_with_retry(
            "POST", f"{BASE_URL}/dynamic-client/", json=payload
        )
        return response.json().get("token")

    def get_dynamic_client_token(self, organization_id: str):
        response = request_with_retry("GET", f"{BASE_URL}/dynamic-client/")

        clients = response.json()
        for client in clients:
            if client.get("organization_id") == organization_id:
                return client.get("token")

        return None


clients = Clients()
