"""
    prefix: /apps/auth/v1/google
"""

import logging
import urllib.parse
import os
import requests
from fastapi import APIRouter, status, Request, Response
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
    description="Authorize Request, retrieves url of google login",
    tags=["auth"],
    status_code=status.HTTP_200_OK,
)
def create_google_auth(request: Request):
    google_auth = GoogleAuth()
    # get google url
    try:
        url, state = google_auth.get_authorization_url()
        # save state to session
        request.session["state"] = state
    except Exception as error:
        logging.error("Authorization url retrieving failed", error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve url",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=url)


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
        return JSONResponse(status_code=400, content="Insufficient Permissions")
    state = request.session["state"]
    parsed_url = urllib.parse.urlparse(str(request.url))
    parsed_url = parsed_url._replace(scheme=os.getenv("SCHEME"))
    parsed_url = parsed_url._replace(netloc=os.getenv("NETLOC"))
    authorization_response = urllib.parse.urlunparse(parsed_url)
    redirect_uri = os.getenv("REDIRECT_URI")
    credentials = google_auth.get_credentials(
        state, authorization_response, redirect_uri
    )
    request.session["credentials"] = google_auth.credentials_to_dict(credentials)
    return Response(status_code=200, content="successfully logged in")


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
    },
)
def revoke(request: Request):
    if "credentials" not in request.session:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="no credentials in session. Login again",
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
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal server error",
        )


@router.get(
    "/logout",
    description="Logs out by deleting the session of credentials",
    tags=["auth"],
    responses={status.HTTP_200_OK: {"description": "Successfully logged out"}},
)
def clear_credentials(request: Request):
    if "credentials" in request.session:
        request.session.pop("credentials")
    return Response(status_code=status.HTTP_200_OK, content="Successfully logged out")


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
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="no credentials in session. Login again",
        )
    elif request.session["credentials"]["refresh_token"] is None:
        request.session.pop("credentials")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content="Refresh token invalid"
        )
    google_auth = GoogleAuth()
    credentials = google_auth.dict_to_credentials(request.session["credentials"])
    user = google_auth.get_user(credentials)
    # TODO: check if user is inside internal DB
    # TODO: if inside db -> return 200 and user info
    # TODO: if not inside db -> put in db -> return 201 and user info
    request.session["credentials"] = google_auth.credentials_to_dict(credentials)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)
