import logging

from fastapi import Request, HTTPException


logger = logging.getLogger(__name__)


def get_token_from_cookies(request: Request):
    token = request.cookies.get("parma_refresh")
    logger.debug("Token from cookies: %s", token)
    if not token:
        raise HTTPException(status_code=401, detail="Token not found in cookies")
    return token
