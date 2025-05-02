from django.test import TestCase
from account.models import User


class AuthTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123",
            account_type="enthusiast"
        )
    
    def test_signup(self):
        signup_data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password1': 'securepass123',
            'password2': 'securepass123',
            'account_type': 'professional'
        }
        
        response = self.client.post('/api/signup/', signup_data)
        self.assertEqual(response.status_code, 200)
        
        # verify user created
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
    
    def test_login(self):
        response = self.client.post('/api/login/', {
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        # check tokens
        self.assertIn('access', response.data)