from app import app
import unittest
import io 
import os 

ppwd=os.getenv('PASSWORD')
class FlaskTestCase(unittest.TestCase):
    # Ensure that flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure Please login in /login page.
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue( b'Please login' in response.data)

    # Ensure can login in /login page.
    def test_can_currect_login_page(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        self.assertIn( b'Upload new File' , response.data,msg=None) 
        self.assertIn( b'Show Local file Table' , response.data,msg=None) 
        self.assertIn( b'show' , response.data,msg=None) 

    # Ensure incurrect login in /login page.
    def test_can_incurrect_login_page(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username="admin", password="xxxx"), 
            follow_redirects=True
        )
        self.assertIn( b'Invalid Credentials. Please try again.' , response.data,msg=None) 

    # Ensure Please login in /welcome page.
    def test_welcome_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/welcome', content_type='application/json')
        self.assertTrue( b'Welcome to Flask!' in response.data)

    # Ensure Please login in /ping page.
    def test_ping_payloads(self):
        tester = app.test_client(self)
        response = tester.get('/ping', content_type='html/text')
        self.assertTrue( b'{"message":"pong!!!"}' in response.data)

    # Ensure logout can use.
    def test_can_secuess_logout_page(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.post(
            '/logout',
            follow_redirects=True
        )
        self.assertIn( b'Welcome to Flask!' , response.data,msg=None)
    
    # Ensure Upload new File in / page.
    def test_home_page_loads(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.get('/', content_type='html/text')
        self.assertTrue( b'Upload new File' in response.data)
        self.assertIn( b'Show Local file Table' , response.data,msg=None) 
        self.assertIn( b'show' , response.data,msg=None)

    # Ensure Upload new File in / page.
    def test_show_page_loads(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.get('/show', content_type='html/text')
        self.assertIn( b'List File' , response.data,msg=None) 

    # Ensure Upload File not in allow file .
    def test_upload_not_allow_type_file(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.post('/uploadfile', data=dict(
            file=(io.BytesIO(b'hi everyone'), 'test.md'),
        ))
        self.assertEqual(response.status_code, 302)
    
    # Ensure Upload file api can use .
    def test_upload_file(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.post('/uploadfile', data=dict(
            file=(io.BytesIO(b'hi everyone'), 'test.txt'),
        ))
        self.assertIn( b'Date' , response.data,msg=None) 

    def test_no_select_file_upload_file(self):
        tester = app.test_client(self)
        from io import BytesIO
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.post('/uploadfile',data=dict(file=(BytesIO(b''),''),follow_redirects=True))
        self.assertEqual(response.status_code, 302)

    def test_download_file(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.get('/downloadfile/.gitkeep')
        self.assertEqual(response.status_code, 200)

    def test_show_buttom(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.post('/',data=dict(show='show'))
        self.assertEqual(response.status_code, 302)

    def test_logout_buttom(self):
        tester = app.test_client(self)
        tester.post(
            '/login',
            data=dict(username="admin", password=ppwd), 
            follow_redirects=True
        )
        response = tester.post('/',data=dict(logout='logout'))
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()