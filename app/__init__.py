from flask import Flask
from .extensions import db
from .students_views import main
from .admin_views import main2,admin

def app(config_file='settings.py'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)

    db.init_app(app)


    app.register_blueprint(main)
    app.register_blueprint(main2)

    admin.init_app(app)

    return app