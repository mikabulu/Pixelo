import django
import os
import sys
from collections import Counter
from datetime import timedelta
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from post.models import Post, Trend

#append extracted hashtags to list of trends 
def extract_hashtags(text, trends):

    for word in text.split():
        if word[0] == '#':
           trends.append(word[1:])

    return trends

#clear existing trends 
Trend.objects.all().delete()

#get all posts from database from last 24h
trends = []
recent_posts = Post.objects.filter(created_at__gte=timezone.now()-timedelta(hours=24))

#loop through posts and extract hashtags
for post in recent_posts:
    extract_hashtags(post.body, trends)

#count the occurences of each hashtag and get 10 most  common 
trends_counter = Counter(trends).most_common(10)
for trend in trends_counter:
    Trend.objects.create(hashtag=trend[0], occurences=trend[1])
    #create new trends based on this
