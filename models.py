"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    firstName = db.Column(db.String(50),
                          nullable=False,
                          unique=True)
    lastName = db.Column(db.String(50), 
                         nullable=False,
                         unique=True)
    imageUrl = db.Column(db.Text, 
                         nullable=True)
    
    post = db.relationship("Post", backref="user")
    
    @property
    def full_name(self):
        return f"{self.firstName} {self.lastName}"
    
class Post(db.Model):
    __tablename__= 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50), 
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    createdAt = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.datetime.now)
    userid = db.Column(db.Integer,
                       db.ForeignKey('users.id'),
                       nullable=False)
    
    @property
    def date(self):
        return self.createdAt.strftime("%a %b %-d  %Y, %-I:%M %p")
