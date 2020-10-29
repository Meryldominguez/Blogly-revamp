from models import db, User, Post
from app import app
import datetime, time

# Create all tables

db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
# Add Users
a = User(first_name="Test1", last_name="User1")
b = User(first_name="Test2", last_name="User2")
c = User(first_name="Test3", last_name="User3")
d = User(first_name="Test4", last_name="User4")
e = User(first_name="Test5", last_name="User5")
f = User(first_name="Test6", last_name="User6")

# Add new objects to session, so they'll persist
db.session.add_all([a,b,c,d])
db.session.commit()

pa = Post(post_title="TestPost1", post_content="User1",author=a)
pb = Post(post_title="TestPost2", post_content="User2",author=b)
pc = Post(post_title="TestPost3", post_content="User1",author=a)
pd = Post(post_title="TestPost4", post_content="User4",author=d)
pe = Post(post_title="TestPost5", post_content="User3",author=c)

# Commit--otherwise, this never gets saved!

db.session.add_all([pa,pb,pc,pd,pe])
db.session.commit()


