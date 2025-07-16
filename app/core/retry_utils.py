from tenacity import (
    retry,
    wait_exponential,
    stop_after_attempt,
    retry_if_exception_type,
)
import requests
from requests.exceptions import Timeout
from fastapi import HTTPException


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=0.5, max=5),
    retry=retry_if_exception_type(Timeout),
    reraise=True,
)
def request_with_retry(method: str, url: str, **kwargs):
    try:
        response = requests.request(method, url, **kwargs)

        if response.status_code == 422:
            detail = "Validation error."
            raise HTTPException(status_code=422, detail=detail)

        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Resource not found.")

        if response.status_code in (400, 401, 500):
            raise HTTPException(
                status_code=502,
                detail=f"External service returned status {response.status_code}",
            )

        response.raise_for_status()
        return response

    except Timeout:
        raise HTTPException(
            status_code=504,
            detail="Timeout: external API did not respond in time.",
        )

    except Exception as err:
        raise HTTPException(status_code=502, detail=f"Unexpected error: {str(err)}")
