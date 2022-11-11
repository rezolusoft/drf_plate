from uuid import uuid4
from django.utils.timezone import datetime, timedelta
import jwt
from django.conf import settings
from hashlib import sha512


def uuid_gen():
    """
    This function return a Universal Unique Identifier
    :return uuid4:
    """
    return uuid4()


def check(key, hash_key):
    """check if the provided key is same with user generated key"""
    if _hash(key) == hash_key:
        return True
    return False


def gen_auth_token(key, user):
    """
    This function generate a JWT token for user authentication
    """
    payload = {
        'username': user.username,
        'key': _hash(key),
        'exp': datetime.utcnow() + timedelta(minutes=60)
    }
    return jwt.encode(payload=payload, key=settings.JWT_SECRET, algorithm='HS256')


def _hash(key):
    return sha512(key.encode()).hexdigest()
