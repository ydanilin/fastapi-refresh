import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = ''
    authjwt_secret_key: str = "secret"
    # SECRET_KEY: bytes = os.urandom(32)
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}


config = Settings()
