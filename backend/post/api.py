from django.http import JsonResponse
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from .models import Post, Like, Comment, Trend 
from .forms import PostForm, AttachmentForm
from rest_framework.decorators import api_view
from account.models import User
from account.serializers import UserSerializer

@api_view(['DELETE'])
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk, created_by=request.user)
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully'})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found or you do not have permission'}, status=403)

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains='#' + trend)

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
    attachment = None
    if request.FILES:
        attachment_form = AttachmentForm(request.POST, request.FILES)
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.created_by = request.user
            attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment: 
            post.attachments.add(attachment)


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

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })

@api_view(['POST'])
def post_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends, many=True)
    return JsonResponse(serializer.data, safe=False)