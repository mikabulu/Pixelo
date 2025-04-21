<template>
  <!-- PROJECT SELECTION -->
  <div class="relative mb-4">
    <select v-model="selectedTag"
      class="p-2 border rounded-md bg-white w-48 mt-2 text-sm text-gray-700 cursor-pointer">
      <option value="">Featured Posts</option>
      <option v-for="tag in tags" :key="tag.id" :value="tag.id">
        {{ tag.name }}
      </option>
    </select>
  </div>

  <div>
    <!-- Loading message -->
    <div v-if="loading" class="w-full bg-white rounded-lg shadow-md p-4 mb-4 text-center">
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
      <div v-for="post in filteredPosts" :key="post.id" class="bg-white rounded-lg shadow-md overflow-hidden">
        <!-- Post Header -->
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
          </div>
          <button @click="openTagSelector(post.id)" class="text-sm text-gray-500">
            Tag Project
          </button>

          <!-- remove from portfolio button (own posts)-->
          <button v-if="isOwnPortfolio" @click="removeFromPortfolio(post.id)"
            class="text-sm text-gray-500 hover:text-[#bfdaa4] flex items-center space-x-1 my-2 mr-2">
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
          <div class="my-3">{{ post.body }}</div>
        </RouterLink>
      </div>
    </div>

    <!-- Tag selector modal -->
    <div v-if="showTagSelector" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-4 rounded-lg max-w-md w-full">
        <h3 class="font-medium mb-3">Add Project Tag</h3>

        <!-- list -->
        <div v-if="tags.length === 0" class="text-center py-2 mb-3">
          <p>No project tags yet</p>
        </div>
        <div v-else class="mb-4 max-h-60 overflow-y-auto">
          <div v-for="tag in tags" :key="tag.id" @click="addTagToPost(tag.id)"
            class="p-2 hover:bg-gray-100 cursor-pointer rounded">
            {{ tag.name }}
          </div>
        </div>

        <!-- new tag -->
        <div class="mb-4">
          <input v-model="newTagName" placeholder="New project name" class="p-2 border rounded w-full mb-2" />
          <button @click="createTag" class="px-3 py-1 bg-green-100 text-green-800 rounded" :disabled="!newTagName">
            Create & Add
          </button>
        </div>

        <div class="flex justify-end">
          <button @click="showTagSelector = false" class="px-3 py-1 bg-gray-100 rounded">
            Cancel
          </button>
        </div>
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
      loading: true,
      selectedTag: '',
      selectedPostId: null,
      showTagSelector: false,
      tags: [],
      newTagName: '',
    }
  },
  computed: {
    isOwnPortfolio() {
      return this.userStore.user.id === this.$route.params.id;
    },
    // all portfolio posts unless tag selected 
    filteredPosts() {
      if (!this.selectedTag) {
        return this.posts;
      }

      console.log('Selected tag:', this.selectedTag);
      console.log('Posts:', this.posts);
      return this.posts.filter(post => {
        console.log('Checking post:', post.id, 'tags:', post.project_tags);
        return post.project_tags &&
          post.project_tags.some(tag => String(tag.id) === String(this.selectedTag));
      });
    }
  },
  watch: {
    showTagSelector(val) {
      if (val) {
        this.loadTags(); //add new tag immediately to tag list
      }
      if (!val) {
        this.getPortfolioPosts(); // refresh posts when modal is closed
      }
    },
    // watch for route changes
    '$route.params.id': {
      handler(newId, oldId) {
        if (newId !== oldId) {
          this.getPortfolioPosts();
        }
      },
      immediate: false
    }
  },
  mounted() {
    this.getPortfolioPosts()
    this.loadTags();
  },
  methods: {
    openTagSelector(postId) {
      this.selectedPostId = postId;
      this.showTagSelector = true;
    },
    loadTags() {
      axios.get(`/api/posts/tags/${this.userStore.user.id}/`)
        .then(response => {
          this.tags = response.data;
        })
        .catch(error => {
          console.log('Error loading tags:', error);
        });
    },
    addTagToPost(tagId) {
      axios.post(`/api/posts/${this.selectedPostId}/tag/${tagId}/`)
        .then(() => {
          this.showTagSelector = false;
          this.selectedPostId = null;
          this.getPortfolioPosts(); // refresh posts after adding tag
        })
        .catch(error => {
          console.log('Error adding tag:', error);
        });
    },
    createTag() {
      if (!this.newTagName) return;

      axios.post('/api/posts/newtag/', { name: this.newTagName })
        .then(response => {
          //add to list, then add to post then clear box 
          this.tags.push(response.data);
          this.addTagToPost(response.data.id);
          this.newTagName = '';
        })
        .catch(error => {
          console.log('Error creating tag:', error);
        });
    },
    getPortfolioPosts() {
      this.loading = true
      axios
        .get(`/api/posts/portfolio/${this.$route.params.id}/`)
        .then(response => {
          console.log('Posts with tags:', response.data.posts);
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
          // filter out removed posts 
          this.posts = this.posts.filter(post => post.id !== postId)
        })
        .catch(error => {
          console.log('Error removing from portfolio', error)
        })
    }
  }
}
</script>