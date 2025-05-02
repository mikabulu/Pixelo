from django.test import TestCase
from rest_framework.test import APIClient
from account.models import User
from .models import Post, Portfolio
from django.core.files.uploadedfile import SimpleUploadedFile
import json

class PortfolioTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123"
        )
        
        # create post 
        self.post = Post.objects.create(
            body="Animation showcase",
            created_by=self.user
        )
        
        # simulate authentication 
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_add_portfolio(self):
        response = self.client.post(f'/api/posts/{self.post.id}/add_to_portfolio/')
        self.assertEqual(response.status_code, 200)
        portfolio = Portfolio.objects.get(user=self.user)
        self.assertTrue(portfolio.posts.filter(id=self.post.id).exists())
    
    def test_create_tag(self):
        response = self.client.post('/api/posts/newtag/', {'name': 'testtag'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'testtag')
    
    def test_post_tag(self):
        #  create a tag
        tag_response = self.client.post('/api/posts/newtag/', {'name': 'testtag'})
        self.assertEqual(tag_response.status_code, 200)
        tag_id = tag_response.json()['id']
        #add to post
        response = self.client.post(f'/api/posts/{self.post.id}/tag/{tag_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('success'))





class MediaUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123"
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_image_upload(self):
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('./testmedia/testimage.png', 'rb').read(),  
            content_type='image/jpeg'
        )

        response = self.client.post(
            '/api/posts/create/',
            {
                'body': 'Post with image',
                'image': image
            },
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(body='Post with image').exists())
        post = Post.objects.get(body='Post with image')
        self.assertTrue(post.attachments.exists())
    
    def test_video_upload(self):
        video = SimpleUploadedFile(
            name='test_video.mp4',
            content=open('./testmedia/testvideo.mp4', 'rb').read(),  
            content_type='video/mp4'
        )

        response = self.client.post(
            '/api/posts/create/',
            {
                'body': 'Post with video',
                'video': video
            },
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(body='Post with video').exists())
        post = Post.objects.get(body='Post with video')
        self.assertTrue(post.attachments.exists())


class FeedTest(TestCase):
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
        
        self.user1.follow(self.user2)
        
        self.post = Post.objects.create(
            body="User2 post",
            created_by=self.user2
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
    
    def test_feed(self):
        response = self.client.get('/api/posts/feed/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1) #check the feed has one post

class LikeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123"
        )
        
        self.post = Post.objects.create(
            body="Test post",
            created_by=self.user
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_like(self):
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db() #refreshpost instance
        self.assertEqual(self.post.likes_count, 1)

class CommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123"
        )
        
        self.post = Post.objects.create(
            body="Test post",
            created_by=self.user
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_comment_post(self):
        response = self.client.post(f'/api/posts/{self.post.id}/comment/', {'body': 'you ate sis!'})
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.comments_count, 1)
