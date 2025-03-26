from .models import Post, Comment
from account.serializers import UserSerializer
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_at_formatted','likes_count', 'comments_count')

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta: 
        model = Comment
        fields = ('id', 'body', 'created_at_formatted', 'created_by')

class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_at_formatted','likes_count', 'comments', 'comments_count') 

        