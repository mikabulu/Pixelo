from django.db import models
import uuid 
from account.models import User
from django.utils.timesince import timesince


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE) #when delete user, delete all likes
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null = True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) #when delete user, delete all likes
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',) #order comments by most recent first
    def created_at_formatted(self):
        return timesince(self.created_at)


class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_images')
    created_by = models.ForeignKey(User, related_name='post_images', on_delete=models.CASCADE) #when delete user, delete all posts



class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null = True) #caption not required
    images = models.ManyToManyField(PostImage, blank=True)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE) 
    class Meta:
        ordering = ('-created_at',) #order posts in feed by most recent first

    def created_at_formatted(self):
        return timesince(self.created_at)

