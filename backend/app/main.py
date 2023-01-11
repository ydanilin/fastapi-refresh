from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from .core.config import config

# https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/
# https://codevoweb.com/restful-api-with-python-fastapi-access-and-refresh-tokens/
# Liba: https://github.com/IndominusByte/fastapi-jwt-auth
# Fork: https://github.com/GlitchCorp/fastapi-another-jwt-auth
app = FastAPI()


class User(BaseModel):
    username: str
    password: str


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return config


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

# A storage engine to save revoked tokens. in production,
# you can use Redis for storage system
denylist = set()


# For this example, we are just checking if the tokens jti
# (unique identifier) is in the denylist set. This could
# be made more complex, for example storing the token in Redis
# with the value true if revoked and false if not revoked
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in denylist


# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@app.post('/login')
def login(
    user: User,
    Authorize: AuthJWT = Depends(),
):
    if user.username != "test@test.com" or user.password != "test":
        raise HTTPException(status_code=401,detail="Bad username or password")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


# Endpoint for revoking the current users access token
@app.delete('/access-revoke')
def access_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    jti = Authorize.get_raw_jwt()['jti']
    denylist.add(jti)
    return {"detail":"Access token has been revoke"}


# Endpoint for revoking the current users refresh token
@app.delete('/refresh-revoke')
def refresh_revoke(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    jti = Authorize.get_raw_jwt()['jti']
    denylist.add(jti)
    return {"detail":"Refresh token has been revoke"}


# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
@app.get('/user')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@app.get('/partially-protected')
def partially_protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()

    # If no jwt is sent in the request, get_jwt_subject() will return None
    current_user = Authorize.get_jwt_subject() or "anonymous"
    return {"user": current_user}
