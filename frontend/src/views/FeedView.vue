<template>
    <div class="max-w-3xl mx-auto p-4">
        <div class="grid grid-cols-1 gap-4">
            <!-- Loading  -->
            <div v-if="isLoading" class="w-full bg-white rounded-lg shadow-md p-4 text-center">
                <p>Loading your feed...</p>
            </div>

            <!-- Empty Feed -->
            <div v-else-if="posts.length === 0" class="w-full bg-white rounded-lg shadow-md p-8 text-center">
                <p class="mb-4">Your feed is empty</p>
                <p class="text-gray-500 text-sm">Follow some users to see their posts here!</p>
            </div>

            <!-- Posts -->
            <div v-else v-for="post in posts" :key="post.id"
                class="w-full bg-white rounded-lg shadow-md p-4 flex flex-col">
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
                        <div class="flex items-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z">
                                </path>
                            </svg>
                            <span class="text-gray-500 text-xs">X likes!</span>
                        </div>

                        <div class="flex items-center space-x-2">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
                                </path>
                            </svg>
                            <span class="text-gray-500 text-xs">X comments</span>
                        </div>
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
    name: 'FeedView',

    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    data() {
        return {
            posts: [],
            isLoading: true
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            this.isLoading = true

            axios
                .get('/api/posts/feed/')
                .then(response => {
                    console.log('Feed data:', response.data)
                    this.posts = response.data
                    this.isLoading = false
                })
                .catch(error => {
                    console.log('Error fetching feed:', error)
                    this.isLoading = false
                })
        }
    }
}
</script>