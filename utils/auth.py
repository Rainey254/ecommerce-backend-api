def check_role(user, role_required):
    """Helper fn to check if the user has required role."""
    if user and 'role' in user:
        return user['role'] == role_required
    
    return False