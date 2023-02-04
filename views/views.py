from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_jwt_extended import jwt_required, create_access_token
import sys
sys.path.append('..')
from models import db, Event, EventSchema, User, UserSchema

event_schema = EventSchema()
user_schema = UserSchema()

# class EventsView(Resource):

#     def get(self,id_event):
#         event= Event.query.get_or_404(id_event)
#         print(event)
#         return event_schema.dump(event)
    
#         # @jwt_required()
#     def delete(self, id_event):
#         event=Event.query_or_404(id_event)
#         db.session.delete(event)
#         db.session.commit()
#         return 'event has been delete it', 204
    


class EventUserView(Resource):

    @jwt_required()
    def post(self, id_user):
        new_event = Event(
            title=request.json['title'],
            category=request.json['category'],
            place=request.json['place'],
            init_date=datetime.strptime(request.json['init_date'],'%m/%d/%y'),
            end_date=datetime.strptime(request.json['end_date'],'%m/%d/%y'),
            modality=request.json['modality'],
            # TODO: check user
        )
        user = User.query.get_or_404(id_user)
        user.events.append(new_event)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'user has an event with the same name',409

        return event_schema.dump(new_event)   
    
    @jwt_required()
    def get(self, id_user):
        user = User.query.get_or_404(id_user)
        return [event_schema.dump(event) for event in user.events]

class EventView(Resource):

    @jwt_required()
    def get(sef,id_event):
        event= Event.query.get_or_404(id_event)
        print(event)
        return event_schema.dump(Event.query.get_or_404(id_event))
    
    @jwt_required()
    def put(self,id_event):
        event=Event.query.get_or_404(id_event)
        event.title = request.json.get('title',event.title)
        event.category = request.json.get('category',event.category)
        event.place = request.json.get('place',event.place)
        event.init_date =datetime.strptime(request.json.get('init_date',event.init_date),'%m/%d/%y') 
        event.end_date = datetime.strptime(request.json.get('end_date',event.end_date),'%m/%d/%y') 
        event.user = request.json.get('user',event.user)
        db.session.commit()
        return event_schema.dump(event)
    
    @jwt_required()
    def delete(self, id_event):
        event=Event.query.get_or_404(id_event)
        db.session.delete(event)
        db.session.commit()
        return event_schema.dump(event)
    
class LogInView(Resource):
    def post(self):
            u_name = request.json["name"]
            u_password = request.json["password"]
            user = User.query.filter_by(name=u_name, password = u_password).first()
            print('user',user)
            access_token= create_access_token(identity=request.json['name'])
            if user:
                return  {'user':user_schema.dump(user),'access_token':access_token}
            else:
                return {'message':'incorrect name or password'}, 401

class SignInView(Resource):
    
    def post(self):
        new_user = User(name=request.json["name"], password=request.json["password"])
        access_token= create_access_token(identity=request.json['name'])
        db.session.add(new_user)
        db.session.commit()
        return {'user':user_schema.dump(new_user),'access_token':access_token}

    def put(self, id_user):
        user = User.query.get_or_404(id_user)
        user.password = request.json.get("password",user.password)
        db.session.commit()
        return user_schema.dump(user)

    def delete(self, id_user):
        user = User.query.get_or_404(id_user)
        db.session.delete(user)
        db.session.commit()
        return '',204