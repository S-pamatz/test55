from ensurepip import bootstrap
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config
from flask_cors import CORS
import os

# Get the directory of the current script file
current_script_directory = os.path.abspath(os.path.dirname(__file__))

# Construct the path to the SSL certificate
ssl_certificate_path = os.path.join(current_script_directory, 'ssl.pem')

# extensions
db = SQLAlchemy()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER


    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:teamFullStack@localhost/our_users1'
    # Azure MySQL database connection details
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin1:CEREO2023!@az-db-cereo.mysql.database.azure.com:3306/our_users1'
#     app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'connect_args': {
#         'ssl': {
#             'ca': ssl_certificate_path
#         }
#     }
# }

    db.init_app(app)
    login.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)

    # Blueprint registration
    from app.Controller.errors import errors_blueprint as errors
    app.register_blueprint(errors)

    from app.Controller.auth_routes import auth_blueprint as auth
    app.register_blueprint(auth)

    from app.Controller.routes import routes_blueprint as routes
    app.register_blueprint(routes)

    return app
