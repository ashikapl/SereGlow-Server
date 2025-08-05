import re
import random

existing_usernames = []

def is_valid_email(email):
    # Simple email regex
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    # At least one lowercase, one uppercase, one digit, one special char, min 8 chars
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password) is not None

def generate_username(first_name, last_name):
    counter =  random.randint(1, 9)
    username = f"{first_name.lower()}_{counter}{last_name.lower()[:3]}"

    while username in existing_usernames:
        username = f"{first_name.lower()}_{counter}{last_name.lower()[:3]}"
        counter = random.randint(1, 9)

    existing_usernames.append(username)
    return username