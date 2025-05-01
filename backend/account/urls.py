from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api

urlpatterns = [
    path('me/', api.me, name='me'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', api.signup, name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('logout/', api.logout, name='logout'),
    path('followers/stats/<uuid:user_id>/', api.follower_stats, name='follower_stats'),
    path('followers/check/<uuid:user_id>/', api.check_follow_status, name='check_follow_status'),
    path('followers/follow/<uuid:user_id>/', api.follow_user, name='follow_user'),
    path('followers/unfollow/<uuid:user_id>/', api.unfollow_user, name='unfollow_user'),
    path('editprofile/', api.edit_profile, name='edit_profile'),
    path('followers/list/<uuid:user_id>/', api.followers_list, name='followers_list'),
    path('following/list/<uuid:user_id>/', api.following_list, name='following_list'),
]