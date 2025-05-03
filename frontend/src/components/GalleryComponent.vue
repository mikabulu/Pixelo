<template>
  <div class="p-4">
    <div class="columns-2 md:columns-3 lg:columns-4 gap-4 space-y-4">
      <div v-for="post in postsWithAttachments" :key="post.id" class="break-inside-avoid rounded-lg overflow-hidden mb-4">
        <RouterLink :to="{ name: 'postview', params: { id: post.id } }">
          <img v-if="post.attachments[0]?.get_image" :src="post.attachments[0].get_image" class="w-full h-auto block"
            alt="Post image" />
          <video v-else-if="post.attachments[0]?.get_video" controls class="" controlsList="nodownload">
            <source :src="post.attachments[0].get_video" type="video/mp4" />
            Your browser does not support the video.
          </video>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  name: 'GalleryComponent',

  props: {
    propPosts: {
      type: Array,
      default: () => []
    }
  },

  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },

  data() {
    return {
      posts: [],
    }
  },

  computed: {
    postsWithAttachments() {
      // only show posts with attachments
      const filteredPosts = this.posts.length > 0
        ? this.posts.filter(post => post.attachments && post.attachments.length > 0)
        : this.propPosts.filter(post => post.attachments && post.attachments.length > 0)

      return filteredPosts
    }
  },

  mounted() {
    // fetch posts if not passed as prop
    if (this.propPosts.length === 0) {
      this.fetchPosts()
    } else {
      this.posts = this.propPosts
    }
  },
  watch: {
    '$route.params.id': {
      handler(newId, oldId) {
        if (newId !== oldId) {
          this.fetchPosts() 
        }
      },
      immediate: false
    },
    propPosts: { //filter posts (dropdown in portfoliocomponent )
    handler(newValue) {
      this.posts = newValue;
    },
    deep: true
  }
  },
  methods: {
    fetchPosts() {
      const userId = this.$route.params.id
      axios
        .get(`/api/posts/profiles/${userId}/`)
        .then(response => {
          this.posts = response.data.posts
        })
        .catch(error => {
          console.error('Error fetching posts for gallery:', error)
        })
    }
  }
}
</script>
  
