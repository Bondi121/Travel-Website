from flask import Flask
import os
from app_folder.blueprints.auth.views import users
from app_folder.blueprints.pages.views import pages
from app_folder.extensions import db,migrate,login_manager, mail


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.register_blueprint(users)
    app.register_blueprint(pages)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    return app


   # flask --app views.py --debug run
