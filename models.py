"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    app.app_context().push()
    db.create_all()

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

@classmethod
def get_full_name(cls, User):
    return f"{User.firstName} {User.lastName}"