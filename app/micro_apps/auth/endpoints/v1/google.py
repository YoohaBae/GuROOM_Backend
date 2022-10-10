"""
    prefix: /apps/auth/v1/google
"""

import logging
import urllib.parse
import os
import requests
from fastapi import APIRouter, status, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.auth.models.user import User

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
    description="Authorize Request: redirects to google authentication page",
    tags=["auth"],
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
def create_google_auth(request: Request):
    google_auth = GoogleAuth()
    # get google url
    url, state = google_auth.get_authorization_url()
    # save state to session
    request.session["state"] = state
    # redirect to authorization of google
    return RedirectResponse(url)


@router.get(
    "/oauth-callback",
    description="Callback of Google Authorization: redirects to get user",
    tags=["auth"],
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
def oauth_callback(request: Request, scope: str):
    google_auth = GoogleAuth()
    sufficient = google_auth.check_for_sufficient_permissions(scope)
    if not sufficient:
        return JSONResponse(status_code=400, content="Insufficient Permissions")
    state = request.session["state"]
    parsed_url = urllib.parse.urlparse(str(request.url))
    parsed_url = parsed_url._replace(scheme="https")
    parsed_url = parsed_url._replace(netloc="guroom.live")
    authorization_response = urllib.parse.urlunparse(parsed_url)
    redirect_uri = os.getenv("REDIRECT_URI")
    credentials = google_auth.get_credentials(
        state, authorization_response, redirect_uri
    )
    request.session["credentials"] = google_auth.credentials_to_dict(credentials)
    return RedirectResponse(request.url_for("get_user"))


@router.get(
    "/revoke",
    description="Deletes the permission granted by the user, similar to deleting account",
    tags=["auth"],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Refresh token was successfully revoked"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Token already expired or revoked"
        },
        status.HTTP_307_TEMPORARY_REDIRECT: {
            "description": "Redirects to /authorize as there are no credentials in session"
        },
    },
)
def revoke(request: Request):
    if "credentials" not in request.session:
        return RedirectResponse(
            "/apps/auth/v1/google" + router.url_path_for("create_google_auth")
        )

    google_auth = GoogleAuth()
    credentials = google_auth.dict_to_credentials(request.session["credentials"])

    revoke = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    status_code = getattr(revoke, "status_code")
    if status_code == status.HTTP_200_OK:
        if "credentials" in request.session:
            request.session.pop("credentials")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    elif status_code == status.HTTP_400_BAD_REQUEST:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Token already expired or revoked.",
        )


@router.get(
    "/logout",
    description="Logs out by deleting the session of credentials",
    tags=["auth"],
    responses={status.HTTP_204_NO_CONTENT: {"description": "Successfully logged out"}},
)
def clear_credentials(request: Request):
    if "credentials" in request.session:
        request.session.pop("credentials")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
def get_user(request: Request):
    if "credentials" not in request.session:
        return RedirectResponse(
            "/apps/auth/v1/google" + router.url_path_for("create_google_auth")
        )
    elif request.session["credentials"]["refresh_token"] is None:
        request.session.pop("credentials")
        return RedirectResponse(
            "/apps/auth/v1/google" + router.url_path_for("create_google_auth")
        )
    google_auth = GoogleAuth()
    credentials = google_auth.dict_to_credentials(request.session["credentials"])
    user = google_auth.get_user(credentials)
    # TODO: check if user is inside internal DB
    # TODO: if inside db -> return 200 and user info
    # TODO: if not inside db -> put in db -> return 201 and user info
    request.session["credentials"] = google_auth.credentials_to_dict(credentials)
    return user
