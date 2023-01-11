#!/bin/bash


export UNITTESTING=1

# poetry run pytest -s -k "create_by_agent or create_by_code"

#poetry run pytest -s tests/login/test_login_access_token.py
poetry run pytest -s -k _revoked_token_ok
