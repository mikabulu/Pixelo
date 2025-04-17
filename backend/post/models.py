from django.db import models
import uuid 
import subprocess
import os 
from account.models import User
from django.utils.timesince import timesince
from django.conf import settings
from cloudinary.models import CloudinaryField



class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE) #when delete user, delete all likes
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null = True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) #when delete user, delete all comments
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',) #order comments by most recent first
    def created_at_formatted(self):
        return timesince(self.created_at)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = CloudinaryField('image', folder ='post_attachments') 
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE) #when delete user, delete all posts

    def get_image(self):
        if self.image:
            if self.image.url.lower().endswith('.gif'):
                return self.image.build_url(transformation=[
                    {'effect': 'loop'}  # this forces infinite looping
                    ])
            return self.image.url
        return ''

class PostMe(models.Model):
    id =    models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null = True) #caption not required
    attachments = models.ManyToManyField(PostAttachment, blank=True)

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
    
class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()

