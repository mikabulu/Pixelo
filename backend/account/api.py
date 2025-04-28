from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import User, Follow
from .serializers import UserSerializer

from .forms import SignupForm, ProfileForm


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar(),
        'bio': request.user.bio,
        'account_type': request.user.account_type,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    """signup data"""
    data = request.data
    
    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
        'account_type': data.get('account_type'),
    })
    
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'success'})
    else:
        # return to frontend 
        return JsonResponse({
            'message': 'error',
            'errors': dict(form.errors.items()) 
        })


@api_view(['GET'])
def follower_stats(request, user_id):
    """get follower and following counts for a user"""
    try:
        user = User.objects.get(id=user_id)
        
        return JsonResponse({
            'followers_count': user.get_followers_count(),
            'following_count': user.get_following_count()
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@api_view(['GET'])
def check_follow_status(request, user_id):
    """check if current user is following another user"""
    try:
        user_to_check = User.objects.get(id=user_id)
        is_following = request.user.is_following(user_to_check)
        
        return JsonResponse({
            'is_following': is_following
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@api_view(['POST'])
def follow_user(request, user_id):
    """follow user"""
    try:
        user_to_follow = User.objects.get(id=user_id)
        
        # check if trying to follow self
        if request.user.id == user_to_follow.id:
            return JsonResponse({'error': 'You cannot follow yourself'}, status=400)
        
        request.user.follow(user_to_follow)
        
        return JsonResponse({
            'success': 'You are now following this user'
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

@api_view(['POST'])
def unfollow_user(request, user_id):
    """unfolow user"""
    try:
        user_to_unfollow = User.objects.get(id=user_id)
        
        if not request.user.is_following(user_to_unfollow):
            return JsonResponse({'error': 'You are not following this user'}, status=400)
        
        request.user.unfollow(user_to_unfollow)
        
        return JsonResponse({
            'success': 'You have unfollowed this user'
        })
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    


@api_view(['POST'])
def logout(request):
    return JsonResponse({'message': 'success'})

@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')
    errors = []
    if User.objects.filter(email=request.data.get('email')).exclude(id=user.id).exists():
        errors.append('Email already exists')
    if User.objects.filter(name__iexact=request.data.get('name')).exclude(id=user.id).exists():
        errors.append('Username already exists')
    if errors:
        return JsonResponse({'message': 'error', 'errors': errors})
    else: 
        print(request.FILES)
        print(request.POST)
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return JsonResponse({'message': 'information updated'})
    
@api_view(['POST'])
def edit_password(request):
    user = request.user
    form = PasswordChangeForm(data = request.POST, user = user)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'password updated'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)
    

#get followers    
@api_view(['GET'])
def followers_list(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        followers = user.get_followers()  
        serializer = UserSerializer(followers, many=True)
        return JsonResponse(serializer.data, safe=False)
    except User.DoesNotExist:
        return JsonResponse([], safe=False)

# get following list 
@api_view(['GET'])
def following_list(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        following = user.get_following()  
        serializer = UserSerializer(following, many=True)
        return JsonResponse(serializer.data, safe=False)
    except User.DoesNotExist:
        return JsonResponse([], safe=False)