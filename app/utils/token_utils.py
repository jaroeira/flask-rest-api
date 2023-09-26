from datetime import datetime, timezone, timedelta
from functools import wraps
import hashlib
import os
from flask import jsonify
from flask_jwt_extended import get_jwt, create_access_token, set_access_cookies, get_jwt_identity, verify_jwt_in_request, jwt_required


def generate_random_hash() -> str:
    random_data = os.urandom(32)
    hash_object = hashlib.sha256(random_data)
    random_hash = hash_object.hexdigest()
    return random_hash

def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)

        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response
    

# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator or has the indicated role

def role_required(role: str):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            verify_jwt_in_request()
            claims = get_jwt()
            if "role" in claims and (claims["role"] == 'admin' or claims["role"] == role):
                return fn(*args, **kwargs)
            else:
                return jsonify(message="Admins only!"), 403

        return decorator

    return wrapper
