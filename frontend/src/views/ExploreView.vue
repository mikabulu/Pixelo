<template>
    <div class="max-w-7xl mx-auto flex justify-center">

        <div class="w-full max-w-4xl space-y-4">
            <!--Search Bar -->
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" class="p-4 flex space-x-4">
                    <input v-model="query" type="search" class="p-4 w-full bg-gray-100 rounded-lg"
                        placeholder="What are you looking for?">

                    <button class="inline-block py-4 px-6 bg-[#bfdaa4] text-black rounded-lg">Search</button>
                </form>
            </div>
            <!--Trends Bar -->
            <TrendsComponent/>
            <!--Users -->
            <div class="p-4 bg-[#bfdaa4] border border-gray-200 rounded-lg grid grid-cols-4 gap-4 h-72 overflow-auto"
                v-if="users.length">
                <div class="w-full min-h-64  bg-white rounded-lg shadow-md pt-6 flex flex-col items-center justify-center"
                    v-for="user in users" v-bind:key="user.id">
                    <img :src="user.get_avatar" class="h-40 w-40 mb-3 rounded-full object-cover">
                    <!--send to user profile when name clicked -->
                    <p><strong>
                            <RouterLink :to="{ name: 'profiles', params: { 'id': user.id } }">{{ user.name }}</RouterLink>
                        </strong></p>
                    <div class="my-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.followers_count || 0 }} {{ user.followers_count === 1 ?
                            'follower' : 'followers' }}</p>
                        <p class="text-xs text-gray-500">{{ user.posts_count || 0 }} {{ user.posts_count === 1 ?
                            'post' : 'posts' }}</p>
                    </div>
                </div>
            </div>

            <!--User Posts -->
            <PostComponent v-for="post in posts" :key="post.id" :post="post" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import PostComponent from '@/components/PostComponent.vue'
import TrendsComponent from '@/components/TrendsComponent.vue'

export default {
    name: 'ExploreView',

    components: {
        PostComponent,
        TrendsComponent
    },

    data() {
        return {
            query: '',
            users: [],
            posts: []
        }
    },
    methods: {
        submitForm() {
            console.log('submitForm', this.query)

            axios
                .post('/api/search/', {
                    query: this.query
                })
                .then(response => {
                    console.log('response:', response.data)
                    this.users = response.data.users
                    this.posts = response.data.posts
                })
                .catch(error => {
                    console.log('error:', error)
                })
        }
    }
}
</script>