from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_jwt_extended import JWTManager
import sys
sys.path.insert(0, '/Users/rverosd/Desktop/cloud/proyecto0/flaskr/models')
sys.path.insert(0, '/Users/rverosd/Desktop/cloud/proyecto0/flaskr/views')
from models import db
from views import  EventView, LogInView, SignInView, EventUserView

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

app= create_app('default')

app_context= app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)

@app.route('/')
def hello_world():
	return 'Hello World!'

# api.add_resource(EventsView,'/events/<int:id_event>')
api.add_resource(EventView,'/event/<int:id_event>')
api.add_resource(SignInView, '/signIn')
api.add_resource(LogInView, '/logIn')
api.add_resource(EventUserView, '/user/<int:id_user>/events')

jwt = JWTManager(app)

if __name__ == "__main__":
	app.run()