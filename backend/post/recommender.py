from collections import defaultdict
from .models import Post, Like


def get_item_based_recommendations(user, max_recommendations=5):
    """item-based collaborative filtering"""
    # get posts the user has already liked
    user_liked_posts = list(Like.objects.filter(created_by=user).values_list('post', flat=True))
    
    # if user hasn't liked anything no recommendations 
    if not user_liked_posts:
        return []
    
    # simple dictionary of post: list of all users who liked it
    post_to_users = {}
    for post in Post.objects.filter(likes_count__gt=0):
        post_to_users[post.id] = set(Like.objects.filter(post=post).values_list('created_by_id', flat=True))
    
    # similarity score for each candidate post (new posts not liked by user)
    post_scores = {}
    for candidate_post_id, users_who_liked_candidate in post_to_users.items():
        # skip posts the user already liked
        if candidate_post_id in user_liked_posts:
            continue
            
        # for each liked post, calculate similarity with the candidate
        for liked_post_id in user_liked_posts:
            if liked_post_id in post_to_users:
                users_who_liked_liked = post_to_users[liked_post_id]
                
                # Jaccard similarity!!
                overlap = len(users_who_liked_candidate.intersection(users_who_liked_liked))
                total_users = len(users_who_liked_candidate.union(users_who_liked_liked))
                
                if total_users > 0:
                    similarity = overlap / total_users
                    
                    # add to the running score for this candidate post
                    if candidate_post_id not in post_scores:
                        post_scores[candidate_post_id] = 0
                    post_scores[candidate_post_id] += similarity
    
    # get the top-scoring posts
    top_posts = sorted(post_scores.items(), key=lambda x: x[1], reverse=True)[:max_recommendations]
    recommended_post_ids = [post_id for post_id, _ in top_posts]
    
    return Post.objects.filter(id__in=recommended_post_ids)

