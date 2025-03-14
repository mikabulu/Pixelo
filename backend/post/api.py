from django.http import JsonResponse
from .serializers import PostSeralizer
from .models import Post
from .forms import PostForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes

@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()

    serializer = PostSeralizer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        serializer = PostSeralizer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'error'}) 