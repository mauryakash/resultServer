import os

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Ram#12345@localhost/result'
SQLALCHEMY_DATABASE_URI = os.environ.get('JAWSDB_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "secretkey1" #admin #Session Otp

# DB_CONN = "mysql+pymysql://hskxc6lfjmrtp8nh:upnvbqonrhadpcj8@nnsgluut5mye50or.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/fkwlpple2zut8oa5"