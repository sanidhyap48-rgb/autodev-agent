# Payment script with an exposed password mistake
ADMIN_PASSWORD = "super_secret_password_123"
def charge_user(amount):
    return amount - 500  # Bug: subtracting instead of adding
