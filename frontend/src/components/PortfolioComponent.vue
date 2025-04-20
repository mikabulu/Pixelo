<template>
  <div>
    <!-- loading -->
    <div v-if="loading" class="w-full bg-white rounded-lg p-4 mb-4 text-center">
      <div class="flex items-center justify-center py-4">
        <span>Loading portfolio...</span>
      </div>
    </div>

    <!-- empty portfolio message-->
    <div v-else-if="posts.length === 0" class="w-full bg-white rounded-lg p-2 mb-4 text-center">
      <div class="flex flex-col items-center justify-center py-8">
        <p class="text-gray-500 mb-2">No portfolio items yet</p>
      </div>
    </div>

    <!-- portfolio items -->
    <div v-else class="space-y-4">
      <div v-for="post in posts" :key="post.id" class="bg-white rounded-lg shadow-md overflow-hidden">
        <!-- Post Header -->
        <div class="p-4 flex items-center justify-between">
          <div class="flex items-center space-x-3">
          </div>
          <!-- remove from portfolio button (own posts) -->
          <button v-if="isOwnPortfolio" @click="removeFromPortfolio(post.id)"
            class="text-sm text-gray-500 hover:text-[#bfdaa4] flex items-center space-x-1">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Remove</span>
          </button>
        </div>

        <!-- Post Content -->
        <RouterLink :to="{ name: 'postview', params: { id: post.id } }">
          <!-- Post Attachments -->
          <template v-if="post.attachments.length">
            <div v-for="attachment in post.attachments" :key="attachment.id">
              <!-- image -->
              <img v-if="attachment.get_image" :src="attachment.get_image" class="w-full">

              <!-- video -->
              <video v-if="attachment.get_video" controls class="w-full">
                <source :src="attachment.get_video" type="video/mp4">
              </video>
            </div>
          </template>

          <!-- post body -->
          <div class ="my-4">{{post.body}}</div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  name: 'PortfolioComponent',
  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },
  data() {
    return {
      posts: [],
      loading: true
    }
  },
  computed: {
    isOwnPortfolio() {
      return this.userStore.user.id === this.$route.params.id;
    }
  },
  mounted() {
    this.getPortfolioPosts()
  },
  methods: {
    getPortfolioPosts() {
      this.loading = true
      axios
        .get(`/api/posts/portfolio/${this.$route.params.id}/`)
        .then(response => {
          this.posts = response.data.posts
          this.loading = false
        })
        .catch(error => {
          console.log('Error loading portfolio posts', error)
          this.loading = false
        })
    },
    removeFromPortfolio(postId) {
      axios
        .post(`/api/posts/${postId}/remove_from_portfolio/`)
        .then(response => {
          // filter out deleted posts 
          this.posts = this.posts.filter(post => post.id !== postId)
        })
        .catch(error => {
          console.log('Error removing from portfolio', error)
        })
    }
  }
}
</script>