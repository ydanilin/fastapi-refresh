from backend.app.core.config import config
from tests.regutils import get_client_auth_header

API_V1_STR = config.API_V1_STR


def test_revoked_token_ok(server):
    payload = {'username': 'test@test.com', 'password': 'test'}
    response = server.post(f'{API_V1_STR}/login', json=payload)
    assert response.status_code == 200
    res = response.json()
    access = res['access_token']
    refresh = res['refresh_token']

    # revoke access
    auth = {'Authorization': f'Bearer {access}'}
    response = server.delete(f'{API_V1_STR}/access-revoke', headers=auth)
    assert response.status_code == 200

    # revoked access did not accepted
    auth = {'Authorization': f'Bearer {access}'}
    response = server.get(f'{API_V1_STR}/user', headers=auth)
    assert response.status_code == 401

    # revoke access
    auth = {'Authorization': f'Bearer {refresh}'}
    response = server.delete(f'{API_V1_STR}/refresh-revoke', headers=auth)
    assert response.status_code == 200

    # now refresh is blocked
    response = server.post(f'{API_V1_STR}/refresh', headers=auth)
    assert response.status_code == 401
