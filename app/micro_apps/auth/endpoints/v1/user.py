import logging
from fastapi import APIRouter, status, Cookie
from fastapi.responses import JSONResponse
from app.micro_apps.auth.services.google_auth import GoogleAuth
from app.micro_apps.auth.models.user import User

router = APIRouter()

logging.Formatter(
    "[%(asctime)s] p%(process)s {%(pathname)s"
    ":%(lineno)d} %(levelname)s - %(message)s",
    "%m-%d %H:%M:%S",
)


@router.get(
    "/google",
    response_model=User,
    responses={
        status.HTTP_200_OK: {
            "description": "User Info retrieved",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/User"}}  # type: ignore  # noqa: E501
            },
        },
        status.HTTP_400_BAD_REQUEST: {"description": "User not found"},
    },
    tags=["users"],
)
def get_google_user(token: str | None = Cookie(default=None)):
    try:
        google_auth = GoogleAuth()
        user, auth = google_auth.authenticate_user(token)
        if not user or not auth:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found."},
            )
        encoded_jwt = google_auth.encode_jwt(auth)
    except Exception as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "User not found."},
        )
    response = JSONResponse(status_code=status.HTTP_200_OK, content=user)
    response.set_cookie(key="token", value=encoded_jwt)
    return response


@router.post(
    "/google",
    response_model=User,
    responses={
        status.HTTP_200_OK: {
            "description": "User Successfully Created",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/User"}}  # type: ignore  # noqa: E501
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Insufficient Permissions were given"
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Authorization Failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "User creation process failure"
        },
    },
    tags=["users"],
)
def create_google_auth():
    try:
        google_auth = GoogleAuth()
        user, auth = google_auth.authorize_user()
        encoded_jwt = google_auth.encode_jwt(auth)
        if not user or not auth:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": "User creation process failure."},
            )
    except Warning as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Insufficient permissions were given."},
        )
    except Exception as error:
        logging.error(error)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Authorization failed."},
        )
    response = JSONResponse(status_code=status.HTTP_200_OK, content=user)
    response.set_cookie(key="token", value=encoded_jwt)
    return response
