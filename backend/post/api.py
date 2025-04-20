from django.http import JsonResponse
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer, PortfolioSerializer
from .models import Post, Like, Comment, Trend, Portfolio
from .forms import PostForm, AttachmentForm
from rest_framework.decorators import api_view
from account.models import User
from account.serializers import UserSerializer
import cloudinary
from cloudinary.uploader import destroy 

@api_view(['DELETE'])
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk, created_by=request.user)
        
        for attachment in post.attachments.all():
            # image deletion from cloudinary
            if attachment.image:
                media_public_id = attachment.image.public_id
                cloudinary.uploader.destroy(media_public_id)
            
            # video deletion from cloudinary
            if attachment.video:
                video_public_id = attachment.video.public_id
                cloudinary.uploader.destroy(video_public_id, resource_type="video")
        
        post.delete()
        return JsonResponse({'message': 'Post and its attachments deleted successfully'})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found or you do not have permission'}, status=403)
    except cloudinary.exceptions.Error as e:
        return JsonResponse({'error': f'Error deleting media from Cloudinary: {str(e)}'}, status=500)
    
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
            
            # Handle video files with special considerations
            if 'video' in request.FILES:
                try:
                    # Apply video-specific options when saving
                    attachment.save()
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=400)
            else:
                # Normal save for images
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

@api_view(['POST'])
def add_to_portfolio(request, pk):
    """Add a post to the user's portfolio"""
    try:
        post = Post.objects.get(pk=pk)

        portfolio, created = Portfolio.objects.get_or_create(user=request.user)
        
        # check if post is already in portfolio
        if portfolio.posts.filter(pk=pk).exists():
            return JsonResponse({'message': 'Post already in portfolio'})
        
        portfolio.posts.add(post)
        
        return JsonResponse({'message': 'Added to portfolio'})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

@api_view(['POST'])
def remove_from_portfolio(request, pk):
    """Remove a post from the user's portfolio"""
    try:
        post = Post.objects.get(pk=pk)
        
        try:
            portfolio = Portfolio.objects.get(user=request.user)
            
            # check if post is in portfolio
            if not portfolio.posts.filter(pk=pk).exists():
                return JsonResponse({'message': 'Post not in portfolio'})
            
            portfolio.posts.remove(post)
            
            return JsonResponse({'message': 'Removed from portfolio'})
        except Portfolio.DoesNotExist:
            return JsonResponse({'error': 'Portfolio not found'}, status=404)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

@api_view(['GET'])
def get_portfolio(request, id):
    """Get a user's portfolio posts"""
    try:
        user = User.objects.get(pk=id)
        
        try:
            portfolio = Portfolio.objects.get(user=user)
            posts = portfolio.posts.all()
            
            # Use the same serializer format as post_list_profile
            posts_serializer = PostSerializer(posts, many=True, context={'request': request})
            user_serializer = UserSerializer(user)
            
            return JsonResponse({
                'posts': posts_serializer.data,
                'user': user_serializer.data
            }, safe=False)
        except Portfolio.DoesNotExist:
            # Return empty posts list if portfolio doesn't exist
            user_serializer = UserSerializer(user)
            return JsonResponse({
                'posts': [],
                'user': user_serializer.data
            }, safe=False)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@api_view(['GET'])
def is_in_portfolio(request, pk):
    """Check if a post is in the user's portfolio"""
    try:
        post = Post.objects.get(pk=pk)
        
        try:
            portfolio = Portfolio.objects.get(user=request.user)
            is_in_portfolio = portfolio.posts.filter(pk=pk).exists()
            
            return JsonResponse({'is_in_portfolio': is_in_portfolio})
        except Portfolio.DoesNotExist:
            return JsonResponse({'is_in_portfolio': False})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)