from django.test import TestCase
from account.models import User
from post.models import Post, Like
from rest_framework.test import APIClient
import json

class RecommendationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com", 
            name="User One",
            password="password1"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", 
            name="User Two",
            password="password2"
        )
        self.user3 = User.objects.create_user(
            email="user3@example.com", 
            name="User Three",
            password="password3"
        )
        
        #  posts
        self.post1 = Post.objects.create(
            body="Post 1 content",
            created_by=self.user1
        )
        self.post2 = Post.objects.create(
            body="Post 2 content",
            created_by=self.user2
        )
        self.post3 = Post.objects.create(
            body="Post 3 content",
            created_by=self.user3
        )
        
        # likes for posts 
        like1 = Like.objects.create(created_by=self.user1)
        self.post2.likes.add(like1)
        self.post2.likes_count += 1
        self.post2.save()
        
        like2 = Like.objects.create(created_by=self.user1)
        self.post3.likes.add(like2)
        self.post3.likes_count += 1
        self.post3.save()
        
        like3 = Like.objects.create(created_by=self.user2)
        self.post3.likes.add(like3)
        self.post3.likes_count += 1
        self.post3.save()
        
        like4 = Like.objects.create(created_by=self.user3)
        self.post3.likes.add(like4)
        self.post3.likes_count += 1
        self.post3.save()


        self.client = APIClient()
        self.client.force_authenticate(user=self.user3)
    
    def test_recommendations_based_on_similarity(self):
        # User3 liked 3
        # User1 liked 2 and 3 
        # User2 liked 3
        # so User3 should get recommended 2

        recommendations_response = self.client.get('/api/explore/recommendations/')
        self.assertEqual(recommendations_response.status_code, 200)
        response = json.loads(recommendations_response.content) #convert to python dict
        self.assertEqual(response[0]['id'], str(self.post2.id))

    

class SearchTest(TestCase):
    def setUp(self):
        
        self.user1 = User.objects.create_user(
            email="user1@example.com", 
            name="Charlie",
            password="password1"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", 
            name="User Two",
            password="password2"
        )

        self.post1 = Post.objects.create(
            body="Charlie Post",
            created_by=self.user1
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user2)

    def test_search_returns_correct_results(self):
        response = self.client.post('/api/explore/search/', {'query': 'Charlie'}, format='json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        # check Charlie appears 
        user_names = [user['name'] for user in data['users']]
        self.assertIn('Charlie', user_names)

        # Check charlie's post appears 
        post_bodies = [post['body'] for post in data['posts']]
        self.assertIn('Charlie Post', post_bodies)



