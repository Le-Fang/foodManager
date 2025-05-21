from functools import wraps
from flask import request, session, jsonify
from http import HTTPStatus
from time import time

def rate_limit(limit: int, interval: int):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_ip = request.remote_addr
            key = f"rate_limit:{user_ip}"
            current_time = time()

            if key not in session:
                session[key] = []

            # Remove outdated request timestamps
            session[key] = [ts for ts in session[key] if current_time - ts < interval]

            if len(session[key]) >= limit:
                return jsonify({"message": "Rate limit exceeded"}), HTTPStatus.TOO_MANY_REQUESTS

            # Add the current request timestamp
            session[key].append(current_time)

            return f(*args, **kwargs)
        return decorated_function
    return decorator