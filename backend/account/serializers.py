from .models import User
from rest_framework import serializers
from post.models import Post

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'followers_count', 'posts_count', 'get_avatar', 'account_type')
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_posts_count(self, obj):
        return Post.objects.filter(created_by=obj).count()
    
