from django.http import JsonResponse
from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer
from rest_framework.decorators import api_view

@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']

    #search for users
    users = User.objects.filter(name__icontains=query).exclude(id=request.user.id) #exclude self in search 
    users_serializer = UserSerializer(users, many=True)

    #search for posts
    posts = Post.objects.filter(body__icontains=query).exclude(created_by=request.user) 
    posts_serializer = PostSerializer(posts, many=True)
    return JsonResponse({
        'users': users_serializer.data, 
        'posts': posts_serializer.data},
        safe=False)