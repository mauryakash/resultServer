import os

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Ram#12345@localhost/result'
SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "secretkey1" #admin #Session Otp
