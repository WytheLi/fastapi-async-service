#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import status
from starlette.exceptions import HTTPException


class CustomException(HTTPException):
    """ 用于捕获已知异常，响应内部状态码 """
    def __init__(self, message: str = 'Bad Request'):
        self.status_code = status.HTTP_200_OK
        self.detail = message


class RequestException(HTTPException):

    def __init__(self, message: str = 'Bad Request'):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = message


class ForbiddenError(HTTPException):

    def __init__(self, message: str = 'Forbidden'):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = message


class NotFoundError(HTTPException):

    def __init__(self, message: str = 'Not Found'):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = message


class ServerError(HTTPException):

    def __init__(self, message: str = 'Internal Server Error'):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = message


class GatewayError(HTTPException):

    def __init__(self, message: str = 'Bad Gateway'):
        self.status_code = status.HTTP_502_BAD_GATEWAY
        self.detail = message


class AuthorizationError(HTTPException):

    def __init__(self, message: str = 'Token is invalid'):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = message

