from django.http import JsonResponse
from .serializers import PostSerializer
from .models import Post, Like
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
    
@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    
    # checks if already liked 
    existing_like = post.likes.filter(created_by=request.user).first()
    
    if existing_like:
        # unlike - remove like 
        post.likes.remove(existing_like)
        existing_like.delete()
        post.likes_count = post.likes_count - 1
        post.save()
        return JsonResponse({'message': 'unliked'})
    else:
        # like - add like 
        like = Like.objects.create(created_by=request.user)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()
        return JsonResponse({'message': 'liked'})
    
@api_view(['GET'])
def post_is_liked(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        is_liked = post.likes.filter(created_by=request.user).exists()
        return JsonResponse({'is_liked': is_liked})
    except Exception as e:
        return JsonResponse({'error': e})