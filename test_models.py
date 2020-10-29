from unittest import TestCase

from app import app
from models import db, User
# from flask_sqlalchemy import SQLAlchemy

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        valid = User(first_name="Marie", last_name="Keeney", image_url="www.lorempicsum.com/100")

        self.assertEqual(valid.get_full_name(), "Marie Keeney")
        self.assertEqual(valid.get_full_name(), valid.first_name+" "+valid.last_name)


class PostModelTestCase(TestCase):
    """Tests for model for Pets."""

    def setUp(self):
        """Clean up any existing posts and users"""
        Post.query.delete()
        User.query.delete()
        user=User(first_name="Marie", last_name="Keeney", image_url="www.lorempicsum.com/100")

        db.session.add(user)
        db.session.commit()

        post = Post(post_title="Testing things is fun", post_content="Lorem ipsum and all that stuff", author=user)

    def tearDown(self):
        """Clean up any fouled transaction."""
        Post.query.delete()
        User.query.delete()
        db.session.rollback()
    

