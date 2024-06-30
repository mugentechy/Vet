
from flask import Flask
from flask_cors import CORS
from .db_con import database_setup




def register_blueprints(app):
    from api.users import users
    app.register_blueprint(users)


def create_app(configuration):
    app = Flask(__name__)
    cors = CORS(app)

    register_blueprints(app)
   
 

    return app


