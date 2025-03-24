from django.http import JsonResponse
from .serializers import PostSerializer
from .models import Post
from .forms import PostForm
from rest_framework.decorators import api_view
from account.models import User
from account.serializers import UserSerializer

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    return JsonResponse({
        'posts': posts_serializer.data, 
        'user': user_serializer.data
        }, safe=False)
           

@api_view(['POST'])  
def post_create(request):
    form = PostForm(request.data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'error'}) 
    
@api_view(['GET'])
def feed(request):
    """
    Get posts from users the current user is following
    """
    try:
        # get users followed 
        following_users = request.user.get_following()
        
        # If not following anyone, return empty list
        if following_users.count() == 0:
            print("User is not following anyone")
            return JsonResponse([], safe=False)
        
        posts = Post.objects.filter(created_by__in=following_users)
        
        # Serialize the posts
        serializer = PostSerializer(posts, many=True)
        
        return JsonResponse(serializer.data, safe=False)
    
    except Exception as e:
        return JsonResponse([], safe=False)