"""
    prefix: /apps/auth/v1/google
"""

import logging
import urllib.parse
import os
import json
import requests
from fastapi import APIRouter, status, Request, Cookie
from fastapi.responses import JSONResponse
from typing import Optional
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.auth.endpoints.models.user import User
from app.micro_apps.auth.services.database import DataBase

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter()
router.secret_key = os.getenv("SECRET_KEY")

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s"
    ":%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


@router.get(
    "/authorize",
    description="Authorize Request, retrieves url of google login",
    tags=["auth"],
    status_code=status.HTTP_200_OK,
)
def create_google_auth():
    google_auth = GoogleAuth()
    # get google url
    try:
        url, state = google_auth.get_authorization_url()
        # save state to cookie
        response = JSONResponse(status_code=status.HTTP_200_OK, content=url)
        response.set_cookie("state", state)
    except Exception as error:
        logging.error("Authorization url retrieving failed", error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve url",
        )
    return response


@router.get(
    "/oauth-callback",
    description="Callback of Google Authorization, Logs in",
    tags=["auth"],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "successfully "}},
)
def oauth_callback(request: Request, scope: str):
    google_auth = GoogleAuth()
    sufficient = google_auth.check_for_sufficient_permissions(scope)
    if not sufficient:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content="Insufficient Permissions"
        )
    state = request.cookies.get("state")
    parsed_url = urllib.parse.urlparse(str(request.url))
    parsed_url = parsed_url._replace(scheme=str(os.getenv("SCHEME")))
    parsed_url = parsed_url._replace(netloc=str(os.getenv("NETLOC")))
    authorization_response = urllib.parse.urlunparse(parsed_url)
    redirect_uri = os.getenv("REDIRECT_URI")
    credentials = google_auth.get_credentials(
        state, authorization_response, redirect_uri
    )
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content="successfully logged in"
    )
    response.set_cookie(
        "credentials", json.dumps(google_auth.credentials_to_dict(credentials))
    )
    return response


@router.get(
    "/revoke",
    description="Deletes the permission granted by the user, similar to deleting account",
    tags=["auth"],
    responses={
        status.HTTP_200_OK: {
            "description": "Refresh token was successfully revoked"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Token already expired or revoked"
        },
    },
)
def revoke(credentials: Optional[str] = Cookie(None)):
    if credentials:
        credentials = json.loads(credentials)
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="no credentials in cookies. Login again",
        )
    google_auth = GoogleAuth()
    credentials = google_auth.dict_to_credentials(credentials)

    revoke = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    status_code = getattr(revoke, "status_code")
    if status_code == status.HTTP_200_OK:
        return JSONResponse(status_code=status.HTTP_200_OK, content="successfully revoked")
    elif status_code == status.HTTP_400_BAD_REQUEST:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Token already expired or revoked.",
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal server error",
        )


@router.get(
    "/user",
    response_model=User,
    description="Retrieves user information, saves it into internal database if first time user",
    tags=["auth"],
    responses={
        status.HTTP_200_OK: {
            "description": "user was already inside database",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/User"}}
            },
        },
        status.HTTP_201_CREATED: {
            "description": "user was added to database",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/User"}}
            },
        },
    },
)
def get_user(credentials: Optional[str] = Cookie(None)):
    if credentials:
        credentials = json.loads(credentials)
        if credentials["refresh_token"] is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content="Refresh token invalid",
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="no credentials in cookie. Login again",
        )
    google_auth = GoogleAuth()
    credentials = google_auth.dict_to_credentials(credentials)
    user = google_auth.get_user(credentials)
    db = DataBase()
    if db.check_user_exists(user.email):
        response = JSONResponse(status_code=status.HTTP_200_OK, content=user)
    else:
        db.save_user(user.email)
        response = JSONResponse(status_code=status.HTTP_201_CREATED, content=user)
    response.set_cookie(
        "credentials", json.dumps(google_auth.credentials_to_dict(credentials))
    )
    return response
