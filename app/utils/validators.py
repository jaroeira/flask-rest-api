import re

def is_valid_email(email: str) -> bool:
    # Regular expression for basic email validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(email_pattern, email):
        return True
    else:
        return False