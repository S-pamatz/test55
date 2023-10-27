from ensurepip import bootstrap
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config
# extensions
db = SQLAlchemy()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:teamFullStack@localhost/our_users1'
   # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:CEREO2023@localhost:3306/mysql'
    # instad of localhost i need ipss
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@remote_server_ip_or_hostname:port/database_name'

    db.init_app(app)
    login.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)

    # blue print reg
    from app.Controller.errors import errors_blueprint as errors
    app.register_blueprint(errors)

    from app.Controller.auth_routes import auth_blueprint as auth
    app.register_blueprint(auth)

    from app.Controller.routes import routes_blueprint as routes
    app.register_blueprint(routes)

    return app
