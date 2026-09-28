import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI='sqlite:///trekking.db'
    SQLALCHEMY_DATABASE_MODIFICATIONS=False