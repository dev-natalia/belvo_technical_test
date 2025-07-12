from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
)
import requests


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=0.5, max=5),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    reraise=True,
)
def request_with_retry(method: str, url: str, **kwargs):
    response = requests.request(method, url, **kwargs)
    response.raise_for_status()
    return response
