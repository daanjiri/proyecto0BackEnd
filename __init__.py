from flask import Flask
from flask_cors import CORS, cross_origin


def create_app(config_name):
    app= Flask(__name__)
    CORS(app)
    cors = CORS(app, resource={
        r"/*":{
            "origins":"*"
        }
    })
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///eventos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

    app.config['JWT_SECRET_KEY']='secret-phrase'
    app.config['PROPAGATE_EXCEPTIONS']=True
    
    return app