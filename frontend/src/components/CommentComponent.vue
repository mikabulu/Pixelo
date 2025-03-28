<!-- PostComponent.vue -->
<template>
    <div class="w-full bg-white rounded-lg shadow-md p-4  flex flex-col">
      <!-- Post Header -->
      <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <img :src="comment.created_by.get_avatar" class="w-[40px] rounded-full">
          <p><strong>
              <RouterLink :to="{ name: 'profiles', params: { 'id': comment.created_by.id } }">
                {{ comment.created_by.name }}
              </RouterLink>
            </strong></p>
        </div>
        <p class="text-gray-600">{{ comment.created_at_formatted }} ago</p>
      </div>
  
      <!-- Comment Content -->
      <p class="">{{ comment.body }}</p>
    </div>
  </template>
  
  <script>  
  export default {
    props: {
      comment: Object
    },
  
  }
  </script>