from collections import defaultdict
from post.models import Post, Like


def get_recommendations(user, max_recommendations):
    """item based recommendation """
    # get posts the user has already liked (get the post ids)
    user_liked_posts = list(Like.objects.filter(created_by=user).values_list('post', flat=True))
    
    # if user hasn't liked anything no recommendations 
    if not user_liked_posts:
        return []
    
    # dictionary of post to users: (key: post ID, value: set of users who liked the post)
    post_to_users = {}
    #only consider posts with at least one like 
    for post in Post.objects.filter(likes_count__gt=0):
        post_to_users[post.id] = set(Like.objects.filter(post=post).values_list('created_by_id', flat=True))

    # dictionary of candidate post (new post not liked by user) to 
    # similarity score: key: post ID, value: score
    post_scores = {}
    for candidate_post_id, users_who_liked_candidate in post_to_users.items():
        # skip posts the user already liked
        if candidate_post_id in user_liked_posts:
            continue
            
        # for each liked post, calculate similarity with the candidate
        for liked_post_id in user_liked_posts:
            #safety check (protect against missing data if post deleted)
            if liked_post_id in post_to_users:
                users_who_liked_liked = post_to_users[liked_post_id] #get users who liked same posts
                
                # Jaccard similarity!!
                overlap = len(users_who_liked_candidate.intersection(users_who_liked_liked))
                total_users = len(users_who_liked_candidate.union(users_who_liked_liked))
                
                if total_users > 0:
                    similarity = overlap / total_users
                    
                    # add to the running score for this candidate post
                    if candidate_post_id not in post_scores:
                        post_scores[candidate_post_id] = 0
                    post_scores[candidate_post_id] += similarity
    
    # add post id and score to array for sorting
    sorted_posts = []
    for post_id, score in post_scores.items():
        sorted_posts.append((post_id, score))

    def get_score(post_score_pair):
        return post_score_pair[1] #return the second item in tuple (just the score)

    # sort the list based on the score in descending order
    sorted_posts.sort(key=get_score, reverse=True)

    # select only top max recommended posts 
    top_posts = sorted_posts[:max_recommendations]

    # extract just post IDs from the sorted list
    recommended_post_ids = [post_id for post_id, _ in top_posts]
    
    return Post.objects.filter(id__in=recommended_post_ids)


