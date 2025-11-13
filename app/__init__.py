from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    key = Config()
    
    app.secret_key = key.flask_key