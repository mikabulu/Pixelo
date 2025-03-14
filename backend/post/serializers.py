from .models import Post
from account.serializers import UserSeralizer
from rest_framework import serializers



class PostSeralizer(serializers.ModelSerializer):
    created_by = UserSeralizer(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)