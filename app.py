"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post

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
    posts = Post.query.order_by(Post.createdAt.desc()).all()
    return redirect("posts/home.html", posts=posts)

@app.route('/users', methods=["GET"])
def users_page():
    users = User.query.order_by(User.lastName, User.firstName).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def users_new_form():
    return render_template("users/form.html")

@app.route('/users/new', methods=["POST"])
def users_new():

    new_user = User(
        firstName=request.form['firstName'],
        lastName=request.form['lastName'],
        imageUrl=request.form['imageUrl']
    )

    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.full_name} added.")
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
    flash(f"User {user.full_name} edited.")
    return redirect("/users")

@app.route('/users/<int:userid>/delete', methods=["POST"])
def users_delete(userid):
    user = User.query.get_or_404(userid)
    
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")
    return redirect("/users")




@app.route('/users/<int:userid>/posts/new')
def posts_new_form(userid):
    user = User.query.get_or_404(userid)
    return render_template("/posts/home.html", user=user)

@app.route('/users/<int:userid>/posts/new', methods=["POST"])
def posts_new(userid):
    user = User.query.get_or_404(userid)
    newPost = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(newPost)
    db.session.commit()
    flash(f"Post '{newPost.title}' added.")

    return redirect(f"/users/{userid}")

@app.route('/posts/<int:postid>/edit')
def posts_edit(postid):
    post = Post.query.get_or_404(postid)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:postid>/edit', methods=["POST"])
def posts_update(postid):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(postid)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.userid}")


@app.route('/posts/<int:postid>/delete', methods=["POST"])
def posts_destroy(postid):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(postid)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.userid}")