from django.test import TestCase
from .models import User
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
import json


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
    
    def test_signup_unique_email(self):
        signup_data = {
            'email': 'test@example.com',  
            'name': 'Second User',             
            'password1': 'password123',
            'password2': 'password123',
            'account_type': 'hobbyist'
            }
    
        response = self.client.post('/api/signup/', signup_data)
        data = json.loads(response.content)
        self.assertEqual(data.get('message'), 'error')
        self.assertEqual(User.objects.filter(email='test@example.com').count(), 1) #one user with this email exists 

   
    def test_login(self):
        response = self.client.post('/api/login/', {
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        # check tokens
        self.assertIn('access', response.data)


class FollowTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            name="User One",
            password="password123"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            name="User Two",
            password="password123"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
    
    def test_follow(self):
        response = self.client.post(f'/api/followers/follow/{self.user2.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user1.is_following(self.user2))
    
    def test_unfollow(self):
        #follow
        response = self.client.post(f'/api/followers/follow/{self.user2.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user1.is_following(self.user2))

        #unfollow
        response = self.client.post(f'/api/followers/unfollow/{self.user2.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user1.is_following(self.user2))


class EditProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123",
            account_type="enthusiast",
            bio="Original bio"
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_edit_profile(self):
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('./testmedia/testimage.png', 'rb').read(),  
            content_type='image/jpeg'
        )

        updated_data = {
            'name': 'Updated Name',
            'email': 'test@example.com',  
            'bio': 'Updated bio content',
            'account_type': 'professional',
            'avatar': image
        }
        
        response = self.client.post(
            '/api/editprofile/', 
            updated_data,
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        
        # check
        self.assertEqual(self.user.name, 'Updated Name')
        self.assertEqual(self.user.bio, 'Updated bio content')
        self.assertEqual(self.user.account_type, 'professional')
        self.assertTrue(self.user.avatar)


