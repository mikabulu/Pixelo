from django.db import models
import uuid 
import subprocess
import os 
from account.models import User
from django.utils.timesince import timesince
from django.conf import settings



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


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE) #when delete user, delete all posts

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''
        
    #loop gifs - even if they have loop count 1 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # save file first 

        file_path = self.image.path
        if file_path.lower().endswith('.gif'):
            temp_path = file_path.replace('.gif', '_looped.gif')
            try:
                subprocess.run(
                    ['convert', file_path, '-loop', '0', temp_path], #loop infintely 
                    check=True
                )
                os.replace(temp_path, file_path)  # replace original gif with looped version 
            except Exception as e:
                print(f'Error processing GIF to loop: {e}')

    



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

