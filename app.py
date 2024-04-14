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

@app.route('/users', methods=["GET"])
def users_page():
    users = User.query.order_by(User.lastName, User.firstName).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template('users/form.html')

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

@app.route('/users/<int:userid>')
def users_show(userid):
    user = User.query.get_or_404(userid)
    return render_template('users/show.html', user=user)

@app.route('/users/<int:userid>/edit')
def users_edit(userid):
    user = User.query.get_or_404(userid)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:userid>/edit', methods=["POST"])
def users_update(userid):
    user = User.query.get_or_404(userid)
    user.firstName=request.form['firstName'],
    user.lastName=request.form['lastName'],
    user.imageUrl=request.form['imageUrl']
    
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:userid>/delete', methods=["POST"])
def users_delete(userid):
    user = User.query.get_or_404(userid)
    
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")