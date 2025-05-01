<template>
  <!-- PROJECT SELECTION -->
  <div class="flex justify-between items-center mb-4 portfolio-mng">
    <div class="flex flex-wrap items-center gap-2">
      <select v-model="selectedTag" class="p-2 border rounded-md bg-white w-48 mt-2 text-sm text-gray-700 cursor-pointer">
        <option value="">All Posts</option>
        <option v-for="tag in tags" :key="tag.id" :value="tag.id">
          {{ tag.name }}
        </option>
      </select>
    </div>

    <!-- tag management  -->
    <button v-if="isOwnPortfolio" @click="showTagManager = true"
      class="mt-2 text-sm text-gray-500 hover:text-[#bfdaa4] flex items-center mng-tag">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
        class="size-6 mr-1">
        <path stroke-linecap="round" stroke-linejoin="round"
          d="M9.568 3H5.25A2.25 2.25 0 0 0 3 5.25v4.318c0 .597.237 1.17.659 1.591l9.581 9.581c.699.699 1.78.872 2.607.33a18.095 18.095 0 0 0 5.223-5.223c.542-.827.369-1.908-.33-2.607L11.16 3.66A2.25 2.25 0 0 0 9.568 3Z" />
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 6h.008v.008H6V6Z" />
      </svg>
      Manage Project Tags
    </button>



    <!-- View toggle -->
    <div class="flex bg-[#bfdaa4] rounded-md p-1">
      <button @click="viewMode = 'list'" class="px-3 py-1 rounded-md text-sm"
        :class="viewMode === 'list' ? 'bg-white shadow-sm' : 'text-gray-500'">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zM3.75 12h.007v.008H3.75V12zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm-.375 5.25h.007v.008H3.75v-.008zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
        </svg>
      </button>
      <button @click="viewMode = 'gallery'" class="px-3 py-1 rounded-md text-sm"
        :class="viewMode === 'gallery' ? 'bg-white shadow-sm' : 'text-gray-500'">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
          class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round"
            d="M2.25 7.125C2.25 6.504 2.754 6 3.375 6h6c.621 0 1.125.504 1.125 1.125v3.75c0 .621-.504 1.125-1.125 1.125h-6a1.125 1.125 0 0 1-1.125-1.125v-3.75ZM14.25 8.625c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v8.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 0 1-1.125-1.125v-8.25ZM3.75 16.125c0-.621.504-1.125 1.125-1.125h5.25c.621 0 1.125.504 1.125 1.125v2.25c0 .621-.504 1.125-1.125 1.125h-5.25a1.125 1.125 0 0 1-1.125-1.125v-2.25Z" />
        </svg>
      </button>
    </div>
  </div>

  <!-- Tag Manager Modal -->
  <div v-if="showTagManager" class="fixed inset-0  backdrop-blur-xs bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-4 rounded-lg max-w-md w-full">
      <h3 class="font-medium mb-4">Manage Project Tags</h3>

      <!-- Tag list  -->
      <div v-if="tags.length === 0" class="text-center py-2 mb-3">
        <p>No project tags yet</p>
      </div>
      <div v-else class="mb-4 max-h-60 overflow-y-auto">
        <div v-for="tag in tags" :key="tag.id" class="flex justify-between items-center p-2 hover:bg-gray-50 rounded">
          <span>{{ tag.name }}</span>
          <button @click="confirmDeleteTag(tag)" class="text-sm text-red-500 hover:text-red-700 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-4 h-4 mr-1">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
            </svg>
            Delete
          </button>
        </div>
      </div>

      <!-- new tag -->
      <div class="mb-4">
        <input v-model="newTagName" placeholder="New tag name" class="p-2 border rounded w-full mb-2" />
        <button @click="createTagOnly" class="px-3 py-1 bg-[#bfdaa4] text-black rounded" :disabled="!newTagName">
          Create Tag
        </button>
      </div>

      <div class="flex justify-end">
        <button @click="showTagManager = false" class="px-3 py-1 bg-gray-100 rounded">
          Close
        </button>
      </div>
    </div>
  </div>

  <!-- tag deletion modal  -->
  <div v-if="showDeleteTagConfirmModal" class="fixed inset-0 backdrop-blur-xs flex items-center justify-center z-50">
    <div class="bg-white border border-gray-200 rounded-lg max-w-md w-full mx-4">
      <div class="p-6 text-center">
        <p class="mb-6">Are you sure you want to delete the "{{ tagToDelete?.name }}" tag?</p>
        <div class="flex justify-center space-x-4">
          <button @click="showDeleteTagConfirmModal = false"
            class="py-2 px-4 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300">
            Cancel
          </button>
          <button @click="deleteTag" class="py-2 px-4 bg-red-500 text-white rounded-lg hover:bg-red-600">
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>


  <!-- List/Gallery view toggle -->
  <div>

    <!-- empty portfolio message-->
    <div v-if="posts.length === 0" class="w-full bg-white rounded-lg p-2 mb-4 text-center">
      <div class="flex flex-col items-center justify-center py-8">
        <p class="text-gray-500 mb-2">No portfolio items yet</p>
      </div>
    </div>

    <!-- Portfolio items  -->
    <div v-else>
      <!-- List View -->
      <div v-if="viewMode === 'list'" class="space-y-4">
        <div v-for="post in filteredPosts" :key="post.id" class="bg-white rounded-lg shadow-md overflow-hidden">
          <!-- Post Header -->
          <div class="flex items-center justify-between">
            <!-- Tag Project -->
            <button v-if="isOwnPortfolio" @click="openTagSelector(post.id)"
              class="text-sm text-gray-500 hover:text-[#bfdaa4] my-2 mx-2">
              Edit Project Tags
            </button>

            <!-- Remove button (right side) -->
            <button v-if="isOwnPortfolio" @click="removeFromPortfolio(post.id)"
              class="text-sm text-gray-500 hover:text-[#bfdaa4] flex items-center space-x-1 mx-2">
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
            <div class="my-3 px-4">{{ post.body }}</div>
          </RouterLink>
        </div>
      </div>

      <!-- Gallery View -->
      <div v-else>
        <GalleryComponent :propPosts="filteredPosts" />
      </div>
    </div>
  </div>

  <!-- edit project tags modal  -->
  <div v-if="showTagSelector" class="fixed inset-0 backdrop-blur-xs bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-4 rounded-lg max-w-md w-full border border-gray-200">
      <h3 class="font-medium mb-3">Edit Project Tags</h3>

      <!-- list -->
      <div v-if="tags.length === 0" class="text-center py-2 mb-3">
        <p>No project tags yet</p>
      </div>
      <div v-else class="mb-4 max-h-60 overflow-y-auto">
        <div v-for="tag in tags" :key="tag.id" @click="addTagToPost(tag.id)"
          class="p-2 hover:bg-[#e8f2d7] cursor-pointer rounded flex justify-between items-center">
          <span>{{ tag.name }}</span>
          <svg v-if="isPostTagged(tag.id)" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
            class="size-6 text-[#bfdaa4]">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>

        </div>
      </div>

      <div class="flex justify-center gap-2">
        <button @click="showTagSelector = false" class="px-3 py-1 bg-gray-100 rounded">
          Done
        </button>
        <button @click="showTagSelector = false" class="px-3 py-1 bg-gray-100 rounded">
          Cancel
        </button>

      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import GalleryComponent from '@/components/GalleryComponent.vue'

export default {
  name: 'PortfolioComponent',
  components: {
    GalleryComponent
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
      selectedTag: '',
      selectedPostId: null,
      showTagSelector: false,
      tags: [],
      newTagName: '',
      showTagManager: false,
      showDeleteTagConfirmModal: false,
      tagToDelete: null,
      viewMode: 'list', // default view mode
      selectedPost: null,
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
      return this.posts.filter(post => {
        return post.project_tags &&
          post.project_tags.some(tag => String(tag.id) === String(this.selectedTag)); //check if tag is in post
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
          this.loadTags();
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
    confirmDeleteTag(tag) {
      this.tagToDelete = tag;
      this.showDeleteTagConfirmModal = true;
    },

    deleteTag() {
      if (!this.tagToDelete) return;

      axios.delete(`/api/posts/tags/${this.tagToDelete.id}/delete/`)
        .then(() => {
          // remove the tag from the local array
          this.tags = this.tags.filter(tag => tag.id !== this.tagToDelete.id);

          // if the deleted tag was selected, reset the tag dropdown
          if (this.selectedTag === this.tagToDelete.id) {
            this.selectedTag = '';
          }

          this.showDeleteTagConfirmModal = false;
          this.tagToDelete = null;

          // refresh posts 
          this.getPortfolioPosts();
        })
        .catch(error => {
          console.log('Error deleting tag:', error);
        });
    },

    createTagOnly() {
      if (!this.newTagName) return;

      axios.post('/api/posts/newtag/', { name: this.newTagName })
        .then(response => {
          this.tags.push(response.data);
          this.newTagName = '';
        })
        .catch(error => {
          console.log('Error creating tag:', error);
        });
    },
    openTagSelector(postId) {
      this.selectedPostId = postId;
      this.showTagSelector = true;
      this.selectedPost = this.posts.find(post => post.id === postId);
    },
    loadTags() {
      const profileUserId = this.$route.params.id; //profile owner id 
      axios.get(`/api/posts/tags/${profileUserId}/`)
        .then(response => {
          this.tags = response.data;
        })
        .catch(error => {
          console.log('Error loading tags:', error);
        });
    },
    isPostTagged(tagId) {
      if (!this.selectedPost || !this.selectedPost.project_tags) {
        return false;
      }
      return this.selectedPost.project_tags.some(tag => String(tag.id) === String(tagId));
    },

    addTagToPost(tagId) {
      // ff the post already has tag, remove it (toggle )
      if (this.isPostTagged(tagId)) {
        axios.post(`/api/posts/${this.selectedPostId}/untag/${tagId}/`)
          .then(() => {
            if (this.selectedPost && this.selectedPost.project_tags) {
              this.selectedPost.project_tags = this.selectedPost.project_tags.filter(tag =>
                String(tag.id) !== String(tagId)
              );
            }
          })
          .catch(error => {
            console.log('Error removing tag:', error);
          });
      } else {
        // add tag
        axios.post(`/api/posts/${this.selectedPostId}/tag/${tagId}/`)
          .then(() => {
            // update local post data
            if (this.selectedPost) {
              if (!this.selectedPost.project_tags) {
                this.selectedPost.project_tags = [];
              }
              // find the tag to add from the tags array
              const tagToAdd = this.tags.find(tag => String(tag.id) === String(tagId));
              if (tagToAdd) {
                this.selectedPost.project_tags.push(tagToAdd);
              }
            }
          })
          .catch(error => {
            console.log('Error adding tag:', error);
          });
      }
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
      axios
        .get(`/api/posts/portfolio/${this.$route.params.id}/`)
        .then(response => {
          console.log('Posts with tags:', response.data.posts);
          this.posts = response.data.posts
        })
        .catch(error => {
          console.log('Error loading portfolio posts', error)
        })
    },
    removeFromPortfolio(postId) {
      axios
        .post(`/api/posts/${postId}/remove_from_portfolio/`)
        .then(response => {
          this.removeTagsFromPost(postId);
          // filter out removed posts 
          this.posts = this.posts.filter(post => post.id !== postId)
        })
        .catch(error => {
          console.log('Error removing from portfolio', error)
        })
    },
    removeTagsFromPost(postId) {
      axios
        .post(`/api/posts/${postId}/remove-all-tags/`)
        .catch(error => {
          console.log('Error removing tags from post:', error);
        });
    }
  }
}
</script>

<style scoped>
@media screen and (max-width: 428px) {

  .portfolio-mng,
  grp-1 {
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
  }

}
</style>