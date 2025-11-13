import re

def validate_fields(username: str, password: str, first_name: str, last_name: str, email: str) -> bool:
    valid_username = re.fullmatch(r"^(?!_)(?!.*_$)[a-zA-Z0-9_]{3,20}$", username)
    valid_password = re.fullmatch(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password)
    valid_email = re.fullmatch(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email)
    valid_xname = re.compile(r"^[A-Za-z '-]+$")
    valid_first_name = re.fullmatch(valid_xname, first_name)
    valid_last_name = re.fullmatch(valid_xname, last_name)
    if not valid_username:
        return False, "Invalid username format"
    if not valid_password:
        return False, "Invalid password format"
    if not valid_email:
        return False, "Invalid email format"
    if not valid_first_name:
        return False, "Invalid name format"
    if not valid_last_name:
        return False, "Invalid name format"
    return True, "Successfully Registered"