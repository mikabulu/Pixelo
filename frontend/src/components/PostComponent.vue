<!-- PostComponent.vue -->
<template>
  <div class="w-full bg-white rounded-lg shadow-md p-4 flex flex-col">
    <!-- Post Header -->
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <img src="../assets/charlie.jpg" class="w-[40px] rounded-full">
        <p><strong>
            <RouterLink :to="{ name: 'profiles', params: { 'id': post.created_by.id } }">
              {{ post.created_by.name }}
            </RouterLink>
          </strong></p>
      </div>
      <p class="text-gray-600">{{ post.created_at_formatted }} ago</p>
    </div>

    <!-- Post Content -->
    <p class="mb-3">{{ post.body }}</p>

    <!-- Comments/Likes -->
    <div class="mt-auto flex justify-between">
      <div class="flex space-x-6">
        <div class="flex items-center space-x-2" @click="toggleLike">
          <svg xmlns="http://www.w3.org/2000/svg" :fill="liked ? 'currentColor' : 'none'" viewBox="0 0 24 24"
            stroke-width="1.5" stroke="currentColor" class="w-6 h-6" :class="{ 'text-red-500': liked }">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z">
            </path>
          </svg>
          <span class="text-gray-500 text-xs">
            {{ post.likes_count }} {{ post.likes_count === 1 ? 'like' : 'likes' }}
          </span>
        </div>

        <div class="flex items-center space-x-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
            class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
            </path>
          </svg>
          <RouterLink :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs">{{ post.comments_count }} comments</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PostComponent',

  props: {
    post: Object
  },

  data() {
    return {
      liked: false
    }
  },

  mounted() {
    this.checkLikeStatus();
  },

  methods: {
    // check if post already liked 
    checkLikeStatus() {
      axios
        .get(`/api/posts/${this.post.id}/is_liked/`)
        .then(response => {
          this.liked = response.data.is_liked;
        })
        .catch(error => {
          console.log('Error checking like status', error);
        });
    },

    // like/unlike post 
    toggleLike() {
      console.log('Toggle like for post:', this.post.id)
      axios
        .post(`/api/posts/${this.post.id}/like/`)
        .then(response => {
          if (response.data.message === 'liked') {
            this.post.likes_count += 1
            this.liked = true
          } else if (response.data.message === 'unliked') {
            this.post.likes_count -= 1
            this.liked = false
          }
        })
        .catch(error => {
          console.log('Error', error)
        })
    }
  }
}
</script>