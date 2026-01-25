from django.test import TestCase

# Create your tests here.
class WebsiteTests(TestCase):
    def test_index_page_requires_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_login_page_loads(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Member Login")

    def test_register_page_loads(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create your Account")
    
    def test_register_user(self):
        response = self.client.post('/register/', {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'name': 'Test User',
            'phone': '1234567890'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")  # Assuming redirect to login page after registration

    def test_login_user(self):
        # First, register the user
        self.client.post('/register/', {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'name': 'Test User',
            'phone': '1234567890'
        })  
        # Then, attempt to log in
        response = self.client.post('/login/', {
            'email': 'testuser',
            'pass': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to index page
        self.assertIn('_auth_user_id', self.client.session)  # Check if user is logged in
    def test_logout_user(self):
        # First, register and log in the user
        self.client.post('/register/', {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'name': 'Test User',
            'phone': '1234567890'
        })
        # Then, attempt to log in
        response = self.client.post('/login/', {
            'email': 'testuser@example.com',
            'pass': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to index page
        self.assertIn('_auth_user_id', self.client.session)  # Check if user is logged in

        # Now, log out the user
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.assertNotIn('_auth_user_id', self.client.session)  # Check if user is logged out
    def test_index_page_after_login(self):
        # First, register and log in the user
        self.client.post('/register/', {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'name': 'Test User',
            'phone': '1234567890'
        })
        # Then, attempt to log in
        response = self.client.post('/login/', {
            'email': 'testuser@example.com',
            'pass': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to index page
        self.assertIn('_auth_user_id', self.client.session)  # Check if user is logged in

        # Now, check the index page after login
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "testuser")  # Check if username is displayed on index page
        