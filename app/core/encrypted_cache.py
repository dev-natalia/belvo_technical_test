import os
from cachetools import TTLCache
from cryptography.fernet import Fernet


class EncryptedCache:
    def __init__(self):
        self.dynamic_client_cache = TTLCache(maxsize=100, ttl=86400)  # 24h
        self.consent_cache = TTLCache(maxsize=100, ttl=3600)  # 1h

        key = os.getenv("CRYPTOGRAPHY_KEY")
        if not key:
            raise ValueError("CRYPTOGRAPHY_KEY environment variable not set.")
        self.cipher = Fernet(key)

    def set_dynamic_client_token(self, organization_id: str, token: str):
        encrypted_token = self.cipher.encrypt(token.encode())
        self.dynamic_client_cache[organization_id] = encrypted_token

    def get_dynamic_client_token(self, organization_id: str):
        encrypted_token = self.dynamic_client_cache.get(organization_id)
        if not encrypted_token:
            return None
        try:
            return self.cipher.decrypt(encrypted_token).decode()
        except Exception:
            return None

    def set_consent(self, user_document: str, token: str, consent_id: str):
        encrypted_token = self.cipher.encrypt(token.encode())
        encrypted_consent_id = self.cipher.encrypt(consent_id.encode())
        self.consent_cache[user_document] = (encrypted_token, encrypted_consent_id)

    def get_consent(self, user_document: str):
        encrypted_pair = self.consent_cache.get(user_document)
        if not encrypted_pair:
            return None, None
        try:
            token = self.cipher.decrypt(encrypted_pair[0]).decode()
            consent_id = self.cipher.decrypt(encrypted_pair[1]).decode()
            return token, consent_id
        except Exception:
            return None, None


cache = EncryptedCache()
