from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Event(db.Model):
    # __tablename__ ='events'

    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200),nullable=False)
    category=db.Column(db.String(200),nullable=False)
    place= db.Column(db.String(200))
    init_date= db.Column(db.DateTime)
    end_date= db.Column(db.DateTime)
    modality=db.Column(db.String(200))
    user=db.Column(db.Integer,db.ForeignKey('user.id'))
    __table_args__ =(db.UniqueConstraint('user','title',name='unique_event_title'),)

    # def __repr__(self) -> str:
    #     return f'{self.id}-{self.title}-{self.category}-{self.place}-{self.init_date}-{self.end_date}-{self.modality}'
    
class User(db.Model):
    # __tablename__ ='users'

    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(32))
    events = db.relationship('Event',cascade='all, delete, delete-orphan')
   
    # def __repr__(self) -> str:
    #     return f'{self.id}-{self.name}-{self.password}'
    
class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Event
        include_relationships= True
        load_instance= True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= User
        include_relationships= True
        load_instance= True