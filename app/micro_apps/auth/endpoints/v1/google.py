"""
    prefix: /apps/auth/v1/google
"""

import logging
import os
from fastapi import APIRouter, status, Depends, Body
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from app.micro_apps.auth.endpoints.models.user import User
from app.micro_apps.auth.services import service

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

router = APIRouter()
router.secret_key = os.getenv("SECRET_KEY")


@router.get(
    "/authorize",
    description="Authorize Request, retrieves url of google login",
    tags=["auth"],
    status_code=status.HTTP_200_OK,
)
def create_google_auth():
    # get google url
    url = service.get_google_auth_url()
    if url is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to retrieve url",
        )
    return JSONResponse(status_code=status.HTTP_200_OK, content=url)


@router.post("/login")
def login(body=Body(...), authorize: AuthJWT = Depends()):
    code = body["code"]
    token = service.get_google_token(code)
    if token is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="token creation failed",
        )
    access_token = authorize.create_access_token(subject=token["access_token"])
    refresh_token = authorize.create_refresh_token(subject=token["refresh_token"])
    response = JSONResponse(
        status_code=status.HTTP_201_CREATED, content="token successfully created"
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

    user = service.get_google_user(access_token)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content="user not found"
        )

    exists = service.check_user_existence(user["email"])
    if exists is None:
        # unable to locate user
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="unable to create user")
    elif exists:
        # user exists in our database
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)
    else:
        # new user
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=user)


@router.post("/refresh")
def refresh_token(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    refresh_token = authorize.get_jwt_subject()
    authorize.unset_access_cookies()

    new_token = service.refresh_google_access_token(refresh_token)
    if new_token is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="failed to refresh access token"
        )

    new_access_token = new_token["access_token"]
    new_access_token = authorize.create_access_token(new_access_token)
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content="access token refreshed"
    )
    authorize.set_access_cookies(new_access_token, response)
    return response


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

    revoked = service.revoke_google_token(access_token)
    if not revoked:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="unable to revoke token",
        )
    response = JSONResponse(status_code=status.HTTP_200_OK, content="token revoked")
    authorize.unset_jwt_cookies()
    return response
