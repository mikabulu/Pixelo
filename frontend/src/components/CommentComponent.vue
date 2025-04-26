<template>
  <div class="w-full bg-white rounded-lg shadow-md p-4 flex flex-col">
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <img :src="comment.created_by.get_avatar" class="w-[40px] rounded-full">
        <p><strong>
            <RouterLink :to="{ name: 'profiles', params: { 'id': comment.created_by.id } }">
              {{ comment.created_by.name }}
            </RouterLink>
          </strong></p>
      </div>
      
      <div class="flex items-center space-x-3">
        <p class="text-gray-600">{{ comment.created_at_formatted }} ago</p>
        
        <!-- Delete button (own posts or commenter )-->
        <button 
          v-if="canDelete" 
          @click="showDeleteConfirmModal = true"
          class="text-gray-500 hover:text-red-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Comment Content -->
    <p class="">{{ comment.body }}</p>
    
    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmModal" class="fixed inset-0 backdrop-blur-xs flex items-center justify-center z-50">
      <div class="bg-white border border-gray-200 rounded-lg max-w-md w-full mx-4">
        <div class="p-6 text-center">
          <p class="mb-6">Are you sure you want to delete this comment?</p>
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
  props: {
    comment: Object,
    postOwnerId: String, // pass post owner's ID to check if user can delete comment
  },
  setup() {
    const userStore = useUserStore()
    return {
      userStore
    }
  },
  data() {
    return {
      showDeleteConfirmModal: false
    }
  },
  computed: {
    canDelete() {
      // delete if comment owner or post author 
      return this.userStore.user.id === this.comment.created_by.id || 
             this.userStore.user.id === this.postOwnerId;
    }
  },
  methods: {
    confirmDelete() {
      axios.delete(`/api/posts/comments/${this.comment.id}/delete/`)
        .then(response => {
          this.showDeleteConfirmModal = false;
          // notify parent component 
          this.$emit('commentDeleted', this.comment.id);
        })
        .catch(error => {
          console.log('Error deleting comment:', error);
        });
    }
  }
}
</script>