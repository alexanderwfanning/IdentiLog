from datetime import datetime
import os
def user_logging(username: str, info: str):
    current_datetime = datetime.now()
    filename = f'userlogs/{username}.log'
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a') as file:
        file.write(f'{current_datetime} - {username} - {info}\n')