import jwt
from datetime import datetime
from django.conf import settings

def create_access_token(user_id):
    payload = {
        "user_id": user_id,
        "type": "access",
        "exp": datetime.utcnow() + settings.ACCESS_TOKEN_LIFETIME,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id):
    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": datetime.utcnow() + settings.REFRESH_TOKEN_LIFETIME,
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token):
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
