import os
from datetime import timedelta


class Config:
    SECRET_KEY = 'sofian'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/jepara_e_transport'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'sofian'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=9)
