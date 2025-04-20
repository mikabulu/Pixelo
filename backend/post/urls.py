from django.urls import path
from . import api

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('profiles/<str:id>/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('feed/', api.feed, name='feed'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_delete'),
    path('<uuid:pk>/is_liked/', api.post_is_liked, name='post_is_liked'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('<uuid:pk>/comment/', api.post_comment, name='post_comment'),
    path('trends/', api.get_trends, name='get_trends'),
    path('portfolio/<str:id>/', api.get_portfolio, name='get_portfolio'),
    path('<uuid:pk>/add_to_portfolio/', api.add_to_portfolio, name='add_to_portfolio'),
    path('<uuid:pk>/remove_from_portfolio/', api.remove_from_portfolio, name='remove_from_portfolio'),
    path('<uuid:pk>/is_in_portfolio/', api.is_in_portfolio, name='is_in_portfolio'),
    
] 