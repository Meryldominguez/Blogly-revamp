from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db.drop_all()
db.create_all()


class UsersViewsTestCase(TestCase):
    """Tests for Users."""

    def setUp(self):
        """Add sample user."""
        Post.query.delete()
        User.query.delete()
        

        user = User(first_name="Testuser",last_name="Usertest", image_url="www.lorempicsum.com/100")
        db.session.add(user)
        db.session.commit()

        user= User.query.one()
        post = Post(post_title="Testuser Wrote this thing" , post_content="They wrote something here too", author= user)

        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 302)

    def test_list_users(self):
        with app.test_client() as client:

            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testuser Usertest', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Testuser Usertest</h1>', html)

    def test_view_new_user(self):
        with app.test_client() as client:
            resp= client.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>Add User</h2>", html)

    def test_add_new_user(self):
        with app.test_client() as client:
            formdata = {'first_name':"Testuser2" , 'last_name':"Usertest2" , 'image_url': "www.lorempicsum.com/300"}
            resp = client.post("/users/new", data=formdata, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            usercount = User.query.count()
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Testuser2 Usertest2", html)
            self.assertEqual(usercount, 2)


    def test_view_edit_user(self):
        with app.test_client() as client:
            resp= client.get(f"/users/{self.user_id}/edit")
            user = User.query.one()
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>Edit User {user.full_name}</h1>", html)

    def test_edit_user(self):
        with app.test_client() as client:

            formdata = {'first_name':"edited" , 'last_name':"edited" , 'image_url': "www.lorempicsum.com/300"}

            resp = client.post(f"/users/{self.user_id}/edit", data=formdata, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edited Edited", html)

    def test_view_new_post(self):
        with app.test_client() as client:
            resp= client.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>Add User</h2>", html)

    def test_add_new_post(self):
        with app.test_client() as client:
            user = User.query.get(self.user_id)

            formdata = {'post_title':"Testuser Wrote this SECOND post" , 'post_content':"They wrote a SECOND something here too", 'author': user}
            resp= client.post(f"/users/{self.user_id}/posts/new", data=formdata, follow_redirects=True)

            html = resp.get_data(as_text=True) 

            postcount = Post.query.count()
            post2 = Post.query.all()[1]
          
            self.assertEqual(resp.status_code, 200)   
            self.assertEqual(postcount, 2)   
            self.assertIn(f"{post2.post_title}", html)        
            self.assertIn(f"{post2.author.full_name}", html) 

    def test_edit_post(self):
        with app.test_client() as client:
            user = User.query.get(self.user_id)
            post = Post.query.one()

            formdata = {'post_title':"Testuser Wrote this thing EDITED" , 'post_content':"They wrote something here too", 'author': user}
            
            resp= client.post(f"/posts/{post.id}/edit", data=formdata, follow_redirects=True)

            post = Post.query.one()
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{post.author.full_name}", html)
            
    def test_delete_post(self):
        with app.test_client() as client:
            user = User.query.get(self.user_id)
            post = Post.query.one()

            resp= client.post(f"/posts/{post.id}/delete",follow_redirects=True)

            postcount = Post.query.count()
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(postcount, 0)

