from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    user = db.relationship('Feedback', backref='user', cascade='all, delete')

    @classmethod
    def register(cls, username, pwd, email, first, last):
        hashbrown = bcrypt.generate_password_hash(pwd)
        hashbrown_nugget = hashbrown.decode('utf8')
        return cls(username=username, 
                   password=hashbrown_nugget,
                   email=email,
                   first_name=first,
                   last_name=last)
    
    @classmethod
    def authenticate(cls, username, pwd):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False

class Feedback(db.Model):
    __tablename__ = 'feedback'

    fb_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False)
