from django.urls import path
from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('profiles/<str:id>/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('feed/', api.feed, name='feed'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/is_liked/', api.post_is_liked, name='post_is_liked'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('<uuid:pk>/comment/', api.post_comment, name='post_comment'),
    
] 