from rest_framework.authentication import (BaseAuthentication, get_authorization_header)
from rest_framework import exceptions
from core.auth.models import AuthToken
import jwt
from xlib.methods import gen_auth_token, check
from django.conf import settings
from django.contrib.auth import get_user_model


class JWTAuth(BaseAuthentication):
    """
    Custom JWT authentication for authenticate an user
    """
    keyword = 'Bearer'
    token_model = AuthToken
    message = 'Invalid username or password'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            # check out the authorization header integrity
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(self.message)

        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed(self.message)

        try:
            token = auth[1].decode()

        except UnicodeError:
            raise exceptions.AuthenticationFailed(self.message)

        return self.authenticate_credentials(token)

    def authenticate_header(self, request):
        # Return the string that will be use as the value of WWW-Authenticate
        return self.keyword

    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(jwt=token, key=settings.JWT_SECRET, algorithms=['HS256']) # Decode the token
        except(jwt.ExpiredSignatureError, jwt.DecodeError):
            raise exceptions.AuthenticationFailed(self.message)

        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=payload['username'])
        except user_model.DoesNotExist:
            raise exceptions.AuthenticationFailed(self.message)

        try:
            key = user.auth_token.key
        except self.token_model.DoesNotExist:
            raise exceptions.AuthenticationFailed(self.message)

        if not check(key, payload['key']):
            raise exceptions.AuthenticationFailed(self.message)

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Inactive account')
        return user, gen_auth_token(key, user)

    def get_token(self, user):
        auth_token = self.token_model.objects.filter(user=user).first()

        if not auth_token:
            auth_token = self.token_model.objects.create(user=user)

        return gen_auth_token(auth_token.key, user)
