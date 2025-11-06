import os
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('./.env')
class Config:
    def __init__(self):
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path=dotenv_path)
            self.user_db: str = os.getenv('USER_DB')
            self.require_commit = os.getenv('REQUIRE_COMMIT')
            self.db_key = os.getenv('DB_KEY')
            if not self.db_key:
                raise ValueError("'DB_KEY' is not properly set in .env!")
            if not self.require_commit:
                print("'REQUIRE_COMMIT' not specified in .env file. Defaulting to False")
            if not self.user_db:
                raise ValueError("'USER_DB' not specified within .env file!'")
        else:
            raise ValueError(".env file not found!")