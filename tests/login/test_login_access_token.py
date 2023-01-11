from backend.app.core.config import config
from tests.regutils import get_client_auth_header

API_V1_STR = config.API_V1_STR


def test_login_good_passw(server):
    payload = {'username': 'test@test.com', 'password': 'test'}
    response = server.post(f'{API_V1_STR}/login', json=payload)
    assert response.status_code == 200
    res = response.json()
    assert res['access_token']
    assert res['refresh_token']


def test_login_bad_passw(server):
    payload = {'username': 'test@test.com', 'password': 'wrong'}
    response = server.post(f'{API_V1_STR}/login', json=payload)
    assert response.status_code == 401


def test_didnat_pass_token(server):
    response = server.get(f'{API_V1_STR}/user')
    assert response.status_code == 401


def test_user_token_good(server):
    auth = get_client_auth_header(server)
    response = server.get(f'{API_V1_STR}/user', headers=auth)
    assert response.status_code == 200


def test_partially_token_good(server):
    auth = get_client_auth_header(server)
    response = server.get(f'{API_V1_STR}/partially-protected', headers=auth)
    assert response.status_code == 200
    assert response.json()['user'] == 'test@test.com'


def test_partially_no_token(server):
    response = server.get(f'{API_V1_STR}/partially-protected')
    assert response.status_code == 200
    assert response.json()['user'] == 'anonymous'


# def test_login_token_expired(server, modify_to_email_confirmed_client):
#     client, db = modify_to_email_confirmed_client
#     old_expiry = config.ACCESS_TOKEN_EXPIRE_MINUTES
#     config.ACCESS_TOKEN_EXPIRE_MINUTES = 0.05  # 3 seconds
#     auth = get_client_auth_header(server, client)
#     time.sleep(5)  # wait a little bit more to be sure
#     with server as serverok:
#         response = serverok.post(f'{API_V1_STR}/oauth/test-token', headers=auth)
#         config.ACCESS_TOKEN_EXPIRE_MINUTES = old_expiry
#         assert response.status_code == 429
#         assert 'expired' in response.json()['detail']
# 
# 
# def test_login_token_good(get_tclient, modify_to_email_confirmed_client):
#     client, db = modify_to_email_confirmed_client
#     auth = get_client_auth_header(get_tclient, client)
#     response = get_tclient.post(f'{API_V1_STR}/oauth/test-token', headers=auth)
#     assert response.status_code == 200
#     assert response.json() == client.id


# def test_login_token_bad(server, modify_to_email_confirmed_client):
#     client, db = modify_to_email_confirmed_client
#     auth = get_client_auth_header(server, client)
#     bearer = auth['Authorization']
#     auth['Authorization'] = bearer[:-2] + '00'  # make token bad
#     with server as serverok:
#         response = serverok.post(f'{API_V1_STR}/oauth/test-token', headers=auth)
#         assert response.status_code == 403
#         assert 'not validate' in response.json()['detail']
