import jwt
from jwt import exceptions
from datetime import datetime, timedelta, timezone
import os
from flask import request

# Load the secret key from environment variables
SECRET_KEY = os.getenv('SECRET_KEY')

# Helper function to generate a JWT
def generate_jwt(user_id, role, expires_in=3600):
    """
    Generates a JWT with the given user_id and role.
    Args:
        user_id (str): The unique identifier for the user.
        role (str): The role of the user (e.g., 'admin' or 'user').
        expires_in (int): Expiration time in seconds (default: 1 hour).
    Returns:
        str: The encoded JWT.
    """
    expiration = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    payload = {
        'sub': user_id,
        'role': role,
        'exp': expiration  # Add expiration to the payload
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

# Helper function to verify a JWT
def verify_jwt(token):
    """
    Verifies a JWT and returns the decoded payload.
    Args:
        token (str): The JWT to verify.
    Returns:
        dict: The decoded payload if the token is valid.
    Raises:
        jwt.ExpiredSignatureError: If the token has expired.
        jwt.InvalidTokenError: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except exceptions.ExpiredSignatureError:
        raise exceptions.ExpiredSignatureError("Token has expired")
    except exceptions.InvalidTokenError:
        raise exceptions.InvalidTokenError("Invalid token")

# Helper function to check the user's role
def check_role(token, role_required):
    """
    Checks if the user has the required role based on their JWT.
    Args:
        token (str): The JWT to verify.
        role_required (str): The required role (e.g., 'admin').
    Returns:
        bool: True if the user's role matches the required role, False otherwise.
    """
    try:
        payload = verify_jwt(token)
        return payload.get('role') == role_required
    except (exceptions.ExpiredSignatureError, exceptions.InvalidTokenError):
        return False

# Middleware to extract and verify the token from the Authorization header
def get_token_from_request():
    """
    Extracts the Bearer token from the Authorization header of the request.
    Returns:
        str: The extracted token.
    Raises:
        ValueError: If the token is missing or malformed.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        raise ValueError("Authorization token is missing or invalid")
    return auth_header.split(" ")[1]

# Middleware for role-based access control
def role_required(role):
    """
    Decorator to enforce role-based access control.
    Args:
        role (str): The required role (e.g., 'admin').
    """
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                token = get_token_from_request()
                if not check_role(token, role):
                    return {"error": "Access denied"}, 403
            except ValueError as e:
                return {"error": str(e)}, 401
            return f(*args, **kwargs)
        return wrapper
    return decorator