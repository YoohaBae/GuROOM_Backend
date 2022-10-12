"""
    prefix: /apps/auth/v1/google
"""

import logging
import os
from fastapi import APIRouter, status, Depends, Body
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
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
        url = google_auth.get_authorization_url()
        # save state to cookie
        response = JSONResponse(status_code=status.HTTP_200_OK, content=url)
    except Exception as error:
        logging.error("Authorization url retrieving failed", error)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve url",
        )
    return response


@router.post("/login")
def login(body=Body(...), authorize: AuthJWT = Depends()):
    code = body["code"]
    google_auth = GoogleAuth()
    token = google_auth.get_token(code)
    if token:
        access_token = authorize.create_access_token(subject=token["access_token"])
        refresh_token = authorize.create_refresh_token(subject=token["refresh_token"])
        response = JSONResponse(
            status_code=status.HTTP_201_CREATED, content="token successfully created"
        )
        authorize.set_access_cookies(access_token, response)
        authorize.set_refresh_cookies(refresh_token, response)
        return response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="token creation failed",
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
def get_user(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()
    google_auth = GoogleAuth()
    user = google_auth.get_user(access_token)

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="user not found"
        )

    db = DataBase()
    if db.check_user_exists(user["email"]):
        response = JSONResponse(status_code=status.HTTP_200_OK, content=user)
    else:
        db.save_user(user["email"])
        response = JSONResponse(status_code=status.HTTP_201_CREATED, content=user)
    return response


@router.post("/refresh")
def refresh_token(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    refresh_token = authorize.get_jwt_subject()

    authorize.unset_access_cookies()

    google_auth = GoogleAuth()
    new_token = google_auth.refresh_token(refresh_token)

    if new_token:
        new_access_token = new_token["access_token"]

        new_access_token = authorize.create_access_token(new_access_token)
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content="access token refreshed"
        )
        authorize.set_access_cookies(new_access_token, response)
        return response
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content="failed to refresh access token"
    )


@router.delete("/logout")
def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    authorize.unset_jwt_cookies()
    response = JSONResponse(status_code=status.HTTP_200_OK, content="token deleted")
    return response


@router.delete("/revoke")
def revoke(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    google_auth = GoogleAuth()
    if google_auth.revoke_token(access_token):
        response = JSONResponse(status_code=status.HTTP_200_OK, content="token revoked")
        authorize.unset_jwt_cookies()
        return response
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="unable to revoke token",
    )
