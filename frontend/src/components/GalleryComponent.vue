<template>
  <div class="p-4">
    <div class="columns-2 md:columns-3 lg:columns-4 gap-4 space-y-4">
      <div v-for="post in postsWithAttachments" :key="post.id" class="break-inside-avoid rounded-lg overflow-hidden mb-4">
        <RouterLink :to="{ name: 'postview', params: { id: post.id } }">
          <img v-if="post.attachments[0]?.get_image" :src="post.attachments[0].get_image" class="w-full h-auto block"
            alt="Post image" />
          <video v-else-if="post.attachments[0]?.get_video" controls class="w-full h-auto block">
            <source :src="post.attachments[0].get_video" type="video/mp4" />
            Your browser does not support the video tag.
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
      loading: false
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
          this.fetchPosts() //watch for route changes 
        }
      },
      immediate: false
    }
  },
  methods: {
    fetchPosts() {
      this.loading = true

      const userId = this.$route.params.id

      axios
        .get(`/api/posts/profiles/${userId}/`)
        .then(response => {
          this.posts = response.data.posts
          this.loading = false
        })
        .catch(error => {
          console.error('Error fetching posts for gallery:', error)
          this.loading = false
        })
    }
  }
}
</script>
  
<style scoped>
.columns-2 {
  column-count: 2;
}

@media (min-width: 768px) {
  .md\:columns-3 {
    column-count: 3;
  }
}

@media (min-width: 1024px) {
  .lg\:columns-4 {
    column-count: 4;
  }
}

.break-inside-avoid {
  break-inside: avoid;
}
</style>