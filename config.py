import datetime
import os


class Config:

    # Database
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'groupmedia.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '4310583bffb24e8b9e1db6081d321660'  # uuid.uuid4().hex
    JWT_EXPIRATION_DELTA = datetime.timedelta(days=1)
