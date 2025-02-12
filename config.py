import os

class Config:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "postgresql://Tair:0000@localhost:5432/expenses"   
    SQLALCHEMY_TRACK_MODIFICATIONS = False
