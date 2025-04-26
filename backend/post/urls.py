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
    path('<uuid:pk>/', api.post_view, name='post_detail'),
    path('<uuid:pk>/comment/', api.post_comment, name='post_comment'),
    path('portfolio/<str:id>/', api.get_portfolio, name='get_portfolio'),
    path('<uuid:pk>/add_to_portfolio/', api.add_to_portfolio, name='add_to_portfolio'),
    path('<uuid:pk>/remove_from_portfolio/', api.remove_from_portfolio, name='remove_from_portfolio'),
    path('<uuid:pk>/is_in_portfolio/', api.is_in_portfolio, name='is_in_portfolio'),
    path('item-recommendations/', api.item_based_recommendations, name='item_recommendations'),
    path('item-recommendations/<int:limit>/', api.item_based_recommendations, name='item_recommendations_with_limit'),
    path('tags/<str:user_id>/', api.get_user_tags, name='get_user_tags'),
    path('newtag/', api.create_tag, name='create_new_tag'),
    path('<uuid:post_id>/tag/<int:tag_id>/', api.add_tag_to_post, name='add_tag_to_post'),   
    path('<uuid:post_id>/remove-all-tags/', api.remove_all_tags_from_post, name='remove_all_tags_from_post'),
    path('tags/<int:tag_id>/delete/', api.delete_tag, name='delete_tag'),
    path('comments/<uuid:comment_id>/delete/', api.delete_comment, name='delete_comment'),
    path('<uuid:post_id>/untag/<int:tag_id>/', api.untag_post, name='untag_post'),
] 