from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_socketio import SocketIO
from datetime import datetime

DEV = True
app = Flask(__name__)
# app configuration
app.secret_key = 'cdwyfhbwfilvbehvnewjncyri b9hGGJBANuvbNAJBHBjBCYIBJBAyibunxubiubUBASUBAU'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if DEV:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.debug = True
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kotlsxhypaemki:29aef82064a428c6ca1216afe9cda5259b53a0982afc7d832404f55db6440f02@ec2-3-211-149-196.compute-1.amazonaws.com:5432/dbdt7iphe155rm'
# make socketio for the app
socketio = SocketIO(app, broadcast=True, always_connect=True)
# make database
db = SQLAlchemy(app)


def current_time() -> str:
    """Return current time"""
    return datetime.now().strftime("%d/%m/%Y %H:%M")

#### MODELS FOR DATABASE ####
class Messgae(db.Model):
    """Represent all the messages in the database."""
    id = db.Column(db.Integer, primary_key=True) # id for each message
    username = db.Column(db.String(20), nullable=False) # username that wrote the message
    message = db.Column(db.String(100), nullable=False) # the message
    datetime = db.Column(db.String(16), nullable=False) # when the message was sent

    def __repr__(self) -> str:
        return f'<Message from User {self.username} at {self.datetime}>'

    @staticmethod
    def all_messages():
        """Return all the messages existed"""
        return Messgae.query.all()
    
    @staticmethod 
    def new_id():
        """Make new id"""
        try:
            id_ = Messgae.all_messages()[-1].id
            return id_ + 1
        except:
            # only happened in the first time when there is no messages...
            return 0

    @staticmethod
    def add(username, message):
        """Add message to data base and return the message object"""
        # make message object
        m = Messgae(id=Messgae.new_id(), username=username, message=message, datetime=current_time())
        # add to database
        db.session.add(m)
        db.session.commit()

        return m
    
    @staticmethod
    def delete_all():
        """Delete all the messages from database"""
        msgs = Messgae.all_messages()
        for msg in msgs:
            db.session.delete(msg)
            db.session.commit()
    
    @staticmethod
    def dict_list():
        """Return all messages as dictionary"""
        return [msg.to_dict() for msg in Messgae.all_messages()]
    
    def to_dict(self):
        """Return dictionary of the object"""
        return {"username": self.username, "datetime": self.datetime, "message": self.message}
        
    
class User(db.Model):
    """Represnt all the users in the database"""
    username = db.Column(db.String(20), nullable=False, primary_key=True, unique=False)
    password = db.Column(db.String(20), nullable=False, unique=False)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    @staticmethod
    def find(username):
        """Find user in database according to string username"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def add(username, password):
        """Add user to database if the user does not exists already."""
        if User.find(username) is None:
            u = User(username=username, password=password)
            db.session.add(u)
            db.session.commit()
    
    @staticmethod
    def all_users():
        """return all users"""
        return User.query.all()
    
    @staticmethod
    def delete(usernane='', user_obj=None):
        """Delete user by username or by getting the user object"""
        if usernane != '':
            user_obj = User.find(usernane)
        
        if user_obj is not None:
            db.session.delete(user_obj)
            db.session.commit()
    
    @staticmethod
    def delete_all():
        """Delete all the users from database"""
        users = User.all_users()
        for user in users:
            User.delete(user_obj=user)

# create the database
with app.app_context():
    db.create_all()
# db.create_all()
# User.delete_all()
# Messgae.delete_all()
