import re


def is_email_invalid(email):
    return not re.match(r'\S+@\S+\.\S+', email)


def is_password_invalid(password):
    # Length check
    if len(password) < 8:
        return True

    # Check for at least 1 lowercase and 1 upper case letter
    if password.lower() == password:
        return True

    # Check for at least 1 number
    return not bool(re.search(r'\d', password))


def are_idea_params(impact, ease, confidence):
    if is_between_1_10(impact) and is_between_1_10(ease) and is_between_1_10(confidence):
        return True
    return False


def is_between_1_10(num):
    if num < 1 or num > 10:
        return False
    return True