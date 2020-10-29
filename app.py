"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/")
def home():
    return redirect("/users")

@app.route("/users")
def list_users():
    """Lists users and show add form."""

    users = User.query.order_by(User.last_name,User.first_name)
    posts = Post.query.order_by(Post.id.desc()).limit(5)
    return render_template("list.html", posts=posts,users=users)

@app.route("/users/new", methods=["GET","POST"])
def add_user():
    """Add user and redirect to list."""
    if request.method == "GET":
        return render_template("new_user.html")
    elif request.method=="POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        user = User(first_name=first_name.title(), last_name=last_name.title(), image_url=request.form.get('image_url'))
        db.session.add(user)
        db.session.commit()

        return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET","POST"])
def show_user_edit(user_id):
    """view and edit info on a single user."""
    if request.method =="GET":
        user = User.query.get_or_404(user_id)
        return render_template("edit_user.html", user=user)
    elif request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if not request.form['image_url'] or request.form['image_url']== "None":
            image_url = "https://picsum.photos/200"
        else:
            image_url = request.form['image_url']
        user = User.query.get_or_404(user_id)

        user.first_name=first_name.title()
        user.last_name=last_name.title()
        user.image_url=image_url
        db.session.add(user)
        db.session.commit()
        request.status_code = 200
        return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    request.status_code = 200
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new", methods=["GET","POST"])
def new_posts(user_id):
    """Show and submit new post form."""
    if request.method =="GET":
        user = User.query.get_or_404(user_id)
        return render_template("new_post.html", user=user)
    elif request.method == "POST":
        user = User.query.get_or_404(user_id)
        post_title = request.form['post_title']
        post_content = request.form['post_content']
        post = Post(post_title=post_title, post_content=post_content, author=user)
        db.session.add(post)
        db.session.commit()
        return redirect(f"/users/{user.id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show info single post."""
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["GET","POST"])
def edit_posts(post_id):
    """Show and handle editing for posts."""
    if request.method =="GET":
        post = Post.query.get_or_404(post_id)
        alltags = Tag.query.order_by(Tag.name.desc())
        return render_template("edit_post.html", post=post, tags=alltags)
    elif request.method == "POST":
        post = Post.query.get_or_404(post_id)
        post.post_title = request.form['post_title']
        post.post_content = request.form['post_content']
        
        
        tag_ids = [int(num) for num in request.form.getlist("tag_id")]
        post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        db.session.add(post)
        db.session.commit()
        request.status_code = 200
        return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_posts(post_id):
    """delete posts."""
    post = Post.query.get_or_404(post_id)
    user = post.author.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user}")

@app.route("/tags")
def view_tags():
    """delete posts."""
    tags = Tag.query.all()

    return render_template("tag_list.html", tags=tags)

@app.route("/tags/int:<tag_id>")
def show_tag_detail(tag_id):
    """delete posts."""
    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag_detail.html", tag=tag)

@app.route("/tags/new", methods=["GET","POST"])
def new_tags():
    """delete posts."""
    if request.method =="GET":
        return render_template("new_tag.html")
    elif request.method == "POST":
        tag = Tag(name=request.form['tag_name']) 
        db.session.add(tag)
        db.session.commit()
        request.status_code = 200
        return redirect(f"/tags")

@app.route("/tags/int:<tag_id>/edit", methods=["GET","POST"])
def edit_tag(tag_id):
    """delete posts."""
    if request.method =="GET":
        return render_template("NEWTAGFORM")
    elif request.method == "POST":
        tag = Tag(name=request.form['tag_name']) 
        db.session.add(tag)
        db.session.commit()
        request.status_code = 200
        return redirect(f"/tags")

@app.route("/tags/int:<tag_id>/delete")
def delete_tag(tag_id):
    """delete posts."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    request.status_code = 200
    return redirect(f"/tags")