"""
    prefix: /apps/auth/v1/google
"""

import logging
import os
from fastapi import APIRouter, status, Depends, Body, Response
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.auth.endpoints.models.user import User
from app.services.models.config import Settings
from app.micro_apps.auth.services.database import DataBase

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter()
router.secret_key = os.getenv("SECRET_KEY")

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s"
    ":%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


@AuthJWT.load_config
def get_config():
    return Settings()


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
    access_token = token["access_token"]
    refresh_token = token["refresh_token"]
    response = Response(
        status_code=status.HTTP_201_CREATED,
        content="token successfully created",
        media_type="application/json",
    )
    authorize.set_access_cookies(access_token, response)
    authorize.set_refresh_cookies(refresh_token, response)
    return response


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
    db = DataBase()
    if db.check_user_exists(user["email"]):
        response = JSONResponse(status_code=status.HTTP_200_OK, content=user)
    else:
        db.save_user(user["email"])
        response = JSONResponse(status_code=status.HTTP_201_CREATED, content=user)
    return response


@router.delete("/logout")
def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    authorize.unset_jwt_cookies()
    return JSONResponse(status_code=status.HTTP_200_OK, content="token deleted")


@router.delete("/revoke")
def revoke(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    access_token = authorize.get_jwt_subject()

    google_auth = GoogleAuth()
    if google_auth.revoke_token(access_token):
        authorize.unset_jwt_cookies()
        return JSONResponse(status_code=status.HTTP_200_OK, content="token revoked")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content="unable to revoke token",
    )
