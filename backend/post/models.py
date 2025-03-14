from django.db import models
import uuid 
from account.models import User
from django.utils.timesince import timesince

class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_images')
    created_by = models.ForeignKey(User, related_name='post_images', on_delete=models.CASCADE) #when delete user, delete all posts



class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null = True) #caption not required
    images = models.ManyToManyField(PostImage, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE) 
    class Meta:
        ordering = ('-created_at',) #order posts in feed by most recent first

    def created_at_formatted(self):
        return timesince(self.created_at)
    #likes
    #likes_count 
