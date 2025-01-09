import jwt
from jwt import exceptions
from datetime import datetime, timedelta
import os
from flask import request

# Load the secret key from environment variables
SECRET_KEY = os.getenv('SECRET_KEY')

# Helper function to generate a JWT
def generate_jwt(payload, expires_in=3600):
    """
    Generates a JWT with the given payload and expiration time.
    Args:
        payload (dict): The payload to include in the token.
        expires_in (int): Expiration time in seconds (default: 1 hour).
    Returns:
        str: The encoded JWT.
    """
    expiration = datetime.utcnow() + timedelta(seconds=expires_in)
    payload['exp'] = expiration  # Add expiration to the payload
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