from cachetools import TTLCache
from datetime import timedelta


class Cache:
    def __init__(self):
        self.dynamic_client_cache = TTLCache(maxsize=100, ttl=86400)  # 24h
        self.consent_cache = TTLCache(maxsize=100, ttl=3600)  # 1h

    def set_dynamic_client_token(self, organization_id: str, token: str):
        self.dynamic_client_cache[organization_id] = token

    def get_dynamic_client_token(self, organization_id: str):
        return self.dynamic_client_cache.get(organization_id)

    def set_consent(self, user_document: str, token: str, consent_id: str):
        self.consent_cache[user_document] = token
        self.consent_cache[token] = consent_id

    def get_consent(self, user_document: str):
        token = self.consent_cache.get(user_document)
        consent_id = self.consent_cache.get(token)
        return token, consent_id


cache = Cache()
