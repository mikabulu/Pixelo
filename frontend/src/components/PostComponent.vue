<template>
  <div class="w-full bg-white rounded-lg shadow-md p-4 flex flex-col">
    <!-- Post Header -->
    <div class="mb-4 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full">
        <p><strong>
            <RouterLink :to="{ name: 'profiles', params: { 'id': post.created_by.id } }">
              {{ post.created_by.name }}
            </RouterLink>
          </strong></p>
      </div>
      <p class="text-gray-600 post-time">{{ post.created_at_formatted }} ago</p>
    </div>
    
    <!-- tag! -->
    <div v-if="post.project_tags && post.project_tags.length > 0" class="flex flex-wrap mb-2">
      <RouterLink v-for="tag in post.project_tags" :key="tag.id" :to="{
        name: 'profiles',
        params: { id: post.created_by.id },
        query: { view: 'portfolio', tag: tag.id }
      }" class="text-sm bg-gray-100 hover:bg-[#e8f2d7] rounded-full px-3 py-1 text-gray-700">
        {{ tag.name }}
      </RouterLink>
    </div>

    <template v-if="post.attachments.length">
      <div v-for="attachment in post.attachments" v-bind:key="attachment.id" class="mb-3">
        <!-- image attachment -->
        <img v-if="attachment.get_image" :src="attachment.get_image" class="w-full rounded-lg">

        <!-- video attachment-->
        <video v-if="attachment.get_video" controls class="w-full rounded-lg">
          <source :src="attachment.get_video" type="video/mp4">
        </video>
      </div>
    </template>
    <!-- Post Content -->
    <div v-html="renderHashtags(post.body)" class="post-body my-3"></div>

    <!-- footer section of post  -->
    <div class="mt-auto flex justify-between items-center footer">
      <!-- Comments/Likes -->
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
        <!-- comment icon  -->
        <RouterLink :to="{ name: 'postview', params: { id: post.id } }" class="flex items-center space-x-2 text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
            class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
            </path>
          </svg>
          <span class="text-xs">{{ post.comments_count }} comments</span>
        </RouterLink>

        <!-- Portfolio Button (only for own posts + not for text posts) -->
        <div v-if="userStore.user.id === post.created_by.id && post.attachments.length > 0"
          class="flex items-center space-x-2" @click="togglePortfolio">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
            class="w-6 h-6" :class="{ 'text-[#a9c191]': inPortfolio }">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
          </svg>
          <span class="text-gray-500 text-xs">
            {{ inPortfolio ? 'Remove from Portfolio' : 'Add to Portfolio' }}
          </span>
        </div>
      </div>

      <!-- Trash Icon (only for own posts)-->
      <div class="flex items-center" @click="deletePost" v-if="post.created_by.id === userStore.user.id">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="w-6 h-6 text-gray-500 hover:text-red-500 cursor-pointer">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
        </svg>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmModal" class="fixed inset-0 backdrop-blur-xs flex items-center justify-center z-50">
      <div class="bg-white border border-gray-200 rounded-lg max-w-md w-full mx-4">
        <div class="p-6 text-center">
          <p class="mb-6">Are you sure you want to delete this post? This cannot be undone.</p>
          <div class="flex justify-center space-x-4">
            <button @click="showDeleteConfirmModal = false"
              class="py-2 px-4 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300">
              Cancel
            </button>
            <button @click="confirmDelete" class="py-2 px-4 bg-red-500 text-white rounded-lg hover:bg-red-600">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  name: 'PostComponent',

  props: {
    post: Object
  },
  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },
  data() {
    return {
      liked: false,
      inPortfolio: false,
      showDeleteConfirmModal: false
    }
  },

  mounted() {
    this.checkLikeStatus();
    this.checkPortfolioStatus();
  },

  methods: {
    // delete post
    deletePost() {
      this.showDeleteConfirmModal = true; // show confirmation modal 
    },
    // Called when user confirms deletion in the modal
    confirmDelete() {
      console.log('Delete post:', this.post.id);
      axios
        .delete(`/api/posts/${this.post.id}/delete/`)
        .then(response => {
          console.log('Post deleted successfully', response);
          this.$emit('postDeleted', this.post.id);
          this.showDeleteConfirmModal = false; // Close the modal
        })
        .catch(error => {
          console.log('Error deleting post', error);
        });
    },
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

    // check if post is in portfolio
    checkPortfolioStatus() {
      axios
        .get(`/api/posts/${this.post.id}/is_in_portfolio/`)
        .then(response => {
          this.inPortfolio = response.data.is_in_portfolio;
        })
        .catch(error => {
          console.log('Error checking portfolio status', error);
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
    },

    // add/remove from portfolio
    togglePortfolio() {
      if (this.inPortfolio) {
        // First remove all tags from this post
        axios
          .post(`/api/posts/${this.post.id}/remove-all-tags/`)
          .then(() => {
            // Then remove from portfolio
            return axios.post(`/api/posts/${this.post.id}/remove_from_portfolio/`);
          })
          .then(response => {
            this.inPortfolio = false;
            // Clear the tags array immediately in the frontend
            this.post.project_tags = [];
            this.$emit('postRemoved', this.post.id);
          })
          .catch(error => {
            console.log('Error removing from portfolio', error);
          });
      } else {
        // Add to portfolio
        axios
          .post(`/api/posts/${this.post.id}/add_to_portfolio/`)
          .then(response => {
            this.inPortfolio = true;
          })
          .catch(error => {
            console.log('Error adding to portfolio', error);
          });
      }
    },
    //replace hashtag with clickable link 
    renderHashtags(text) {
      if (!text) return '';
      return text.replace(/#(\w+)/g, '<a href="/hashtags/$1">#$1</a>');
    }
  }
}
</script>

<style scoped>
@media screen and (min-width: 375px) and (max-width: 428px) {
  .footer .text-xs {
    display: none;
  }
  .footer svg {
    width: 1.25rem;
    height: 1.25rem;
  }

  .post-time {
    font-size: 0.75rem;
  }
}
</style>