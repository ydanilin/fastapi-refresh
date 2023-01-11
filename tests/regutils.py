import base64
from typing import Dict

from backend.app.core.config import config

API_V1_STR = config.API_V1_STR


def get_basic_auth_header(login: str, password: str) -> Dict:
    to_encode = f'{login}:{password}'
    encoded = base64.b64encode(to_encode.encode()).decode()
    return {'Authorization': f'Basic {encoded}'}


def get_client_auth_header(server):
    payload = {'username': 'test@test.com', 'password': 'test'}
    response = server.post(f'{API_V1_STR}/login', json=payload)
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}
