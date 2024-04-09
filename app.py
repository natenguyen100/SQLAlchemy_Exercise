"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect('/users')

@app.route('/users')
def users_page():
    users = User.query.all()
    # users = User.query.order_by(User.lastName, User.firstName).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('')

@app.route('/users/new', methods=["POST"])
def users_new():

    new_user = User(
        firstName=request.form['firstName'],
        lastName=request.form['lastName'],
        imageUrl=request.form['imageUrl']
    )

    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/{int:user_id}')

@app.route('/users/{int:user_id}/edit')

@app.route('/users/{int:user_id}', methods=["POST"])

@app.route('/users/{int:user_id}/delete', methods=["POST"])
def users_delete(user_id):
    return redirect("/users")