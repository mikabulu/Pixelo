from django.test import TestCase
from rest_framework.test import APIClient
from account.models import User
from .models import Post, Portfolio, ProjectTag
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
            body="test post",
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
    
    def test_remove_portfolio(self):
        # add to portfolio first
        response = self.client.post(f'/api/posts/{self.post.id}/add_to_portfolio/')
        self.assertEqual(response.status_code, 200)
        portfolio = Portfolio.objects.get(user=self.user)
        self.assertTrue(portfolio.posts.filter(id=self.post.id).exists())
        
        # remove from portfolio
        response = self.client.post(f'/api/posts/{self.post.id}/remove_from_portfolio/')
        self.assertEqual(response.status_code, 200)
        portfolio = Portfolio.objects.get(user=self.user)
        self.assertFalse(portfolio.posts.filter(id=self.post.id).exists())

        # remove all tags
        response = self.client.post(f'/api/posts/{self.post.id}/remove-all-tags/')
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.project_tags.count(), 0)


    

class TagTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123"
        )
        
        # create post 
        self.post = Post.objects.create(
            body="test post",
            created_by=self.user
        )
        
        # simulate authentication 
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_tag(self):
        response = self.client.post('/api/posts/newtag/', {'name': 'testtag'})
        self.assertEqual(response.status_code, 200)
        tag_id = response.json()['id']
        
        # check its in tag list
        tags_response = self.client.get(f'/api/posts/tags/{self.user.id}/')
        self.assertEqual(tags_response.status_code, 200)
        self.assertTrue(ProjectTag.objects.filter(id=tag_id).exists())
    
    def test_delete_tag(self):
        # create tag
        response = self.client.post('/api/posts/newtag/', {'name': 'testtag'})
        self.assertEqual(response.status_code, 200)
        tag_id = response.json()['id']
        
        # delete 
        response = self.client.delete(f'/api/posts/tags/{tag_id}/delete/')
        self.assertEqual(response.status_code, 200)

        # check its not in tag list 
        tags_response = self.client.get(f'/api/posts/tags/{self.user.id}/')
        self.assertEqual(tags_response.status_code, 200)
        self.assertFalse(ProjectTag.objects.filter(id=tag_id).exists())

    
    def test_post_tag(self):
        #  create a tag
        tag_response = self.client.post('/api/posts/newtag/', {'name': 'testtag'})
        self.assertEqual(tag_response.status_code, 200)
        tag_id = tag_response.json()['id']
        #add to post
        response = self.client.post(f'/api/posts/{self.post.id}/tag/{tag_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.post.project_tags.filter(id=tag_id).exists())

    def test_remove_post_tag(self):
        # create tag
        tag_response = self.client.post('/api/posts/newtag/', {'name': 'testtag'})
        self.assertEqual(tag_response.status_code, 200)
        tag_id = tag_response.json()['id']
        
        # add to post
        response = self.client.post(f'/api/posts/{self.post.id}/tag/{tag_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.post.project_tags.filter(id=tag_id).exists())
        
        
        # remove from post
        response = self.client.post(f'/api/posts/{self.post.id}/untag/{tag_id}/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.post.project_tags.filter(id=tag_id).exists())
    
   


class PostTest(TestCase):
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
    
    def test_delete(self):
        # create post 
        self.post = Post.objects.create(
            body="test post",
            created_by=self.user
        )
        #delete
        response = self.client.delete(f'/api/posts/{self.post.id}/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())



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
        is_liked_response = self.client.get(f'/api/posts/{self.post.id}/is_liked/')
        self.assertEqual(is_liked_response.status_code, 200)
    
    def test_unlike(self):
        # like post
        response = self.client.post(f'/api/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, 200)
        is_liked_response = self.client.get(f'/api/posts/{self.post.id}/is_liked/')
        self.assertEqual(is_liked_response.status_code, 200)
        
        #  unlike it
        response = self.client.post(f'/api/posts/{self.post.id}/like/') 
        self.assertEqual(response.status_code, 200)

         #check like is false now 
        is_liked_response = self.client.get(f'/api/posts/{self.post.id}/is_liked/')
        self.assertEqual(is_liked_response.status_code, 200)
        self.assertFalse(is_liked_response.json()['is_liked'])



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

    def test_comment(self):
        response = self.client.post(f'/api/posts/{self.post.id}/comment/', {'body': 'you ate sis!'})
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.comments_count, 1)
    
    def test_delete(self):
        # create comment
        response = self.client.post(f'/api/posts/{self.post.id}/comment/', {'body': 'you ate sis!'})
        self.assertEqual(response.status_code, 200)
        comment_id = response.json()['id']
        
        # delete 
        response = self.client.delete(f'/api/posts/comments/{comment_id}/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.post.comments.filter(id=comment_id).exists())

class HashtagTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            name="Test User",
            password="password123"
        )
        
        self.post = Post.objects.create(
            body="#test",
            created_by=self.user
        )
        self.post = Post.objects.create(
            body="#test",
            created_by=self.user
        )
        self.post = Post.objects.create(
            body="no hashtag",
            created_by=self.user
        )
        self.post = Post.objects.create(
            body="#other",
            created_by=self.user
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_hashtag(self):
        response = self.client.get('/api/posts/?hashtag=test')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        for post in data:
            self.assertIn("#test", post['body'])

