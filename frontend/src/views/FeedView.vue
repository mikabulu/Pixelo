<template>
    <div class="max-w-3xl mx-auto p-4">
        <div class="grid grid-cols-1 gap-4">

            <!-- Empty Feed -->
            <div v-if="posts.length === 0" class="w-full bg-white rounded-lg shadow-md p-8 text-center">
                <p class="mb-4">Your feed is empty</p>
                <p class="text-gray-500 text-sm">Follow some users to see their posts here!</p>
            </div>

            <!-- Posts -->
            <PostComponent v-else v-for="post in posts" :key="post.id" :post="post" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import PostComponent from '@/components/PostComponent.vue' 

export default {
    name: 'FeedView',

    components: {
        PostComponent
    },

    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    data() {
        return {
            posts: [],
        }
    },

    mounted() {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('/api/posts/feed/')
                .then(response => {
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('Error fetching feed:', error)
                })
        }
    }
}
</script>