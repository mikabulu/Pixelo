from .models import Post, Comment, Trend, PostAttachment, Portfolio
from account.serializers import UserSerializer
from rest_framework import serializers


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id', 'get_image', 'get_video')
    
class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    is_in_portfolio = serializers.SerializerMethodField()
    project_tags = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_at_formatted',
                  'likes_count', 'comments_count', 'attachments', 'is_in_portfolio', 'project_tags')
    
    def get_is_in_portfolio(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                portfolio = request.user.portfolio
                return portfolio.posts.filter(id=obj.id).exists()
            except:
                return False
        return False
    
    def get_project_tags(self, obj):
        tags = obj.project_tags.all()
        return [{'id': tag.id, 'name': tag.name} for tag in tags]

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta: 
        model = Comment
        fields = ('id', 'body', 'created_at_formatted', 'created_by')

class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = PostAttachmentSerializer(read_only = True, many=True)
    project_tags = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_at_formatted','likes_count', 'comments', 'comments_count', 'attachments', 'project_tags') 

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences')



class PortfolioSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    
    class Meta:
        model = Portfolio
        fields = ('posts',)

