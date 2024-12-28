import secrets
session_key = secrets.token_hex(32)
print("Your secret session key:", session_key)