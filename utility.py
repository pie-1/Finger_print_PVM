from functools import wraps
from flask import request
def validate_api_key(cache):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('X-API-KEY')
            if not api_key:
                return "Missing Api key", 401

            # Check if API key exists in the cache
            if not cache.get(api_key):
                return "Invalid Api Key", 401

            # Call the decorated function if the API key is valid
            return func(*args, **kwargs)
        return wrapper
    return decorator