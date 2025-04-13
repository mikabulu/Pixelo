from .models import Post, Comment, Trend, PostAttachment
from account.serializers import UserSerializer
from rest_framework import serializers




class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image',)


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only = True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_at_formatted','likes_count', 'comments_count', 'attachments',)

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta: 
        model = Comment
        fields = ('id', 'body', 'created_at_formatted', 'created_by')

class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = PostAttachmentSerializer(read_only = True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_at_formatted','likes_count', 'comments', 'comments_count', 'attachments',) 

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences')

        