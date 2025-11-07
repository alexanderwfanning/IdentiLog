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
            self.admin_username = os.getenv('ADMIN_USERNAME')
            self.admin_password = os.getenv('ADMIN_PASSWORD')
            self.flask_key = os.getenv('FLASK_SECRET_KEY')
            self.organization_key = os.getenv('NEW_USER_PASSWORD')
            self.organization_text = os.getenv('ORGANIZATION_FOOTER_TEXT')
            if not self.db_key:
                raise ValueError("'DB_KEY' is not properly set in .env")
            if not self.require_commit:
                print("'REQUIRE_COMMIT' not specified in .env file. Defaulting to False")
            if not self.user_db:
                raise ValueError("'USER_DB' not specified within .env file'")
            if not self.flask_key:
                raise ValueError("'FLASK_SECRET_KEY' not specified within .env file'")
            if not self.organization_key:
                print("'NEW_USER_PASSWORD' not set in .env file. Users will not be able to register through portal.")
        else:
            raise ValueError(".env file not found!")