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
            
            <!-- Recommendations Section (when not searching) -->
            <div v-if="!isSearching" class="w-full">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="font-semibold text-lg">Recommended For You</h2>
                </div>
                
                <!-- Loading indicator -->
                <div v-if="loadingRecommendations" class="text-center py-4">
                    <p>Loading recommendations...</p>
                </div>
                
                <!-- No recommendations message -->
                <div v-else-if="recommendations.length === 0" class="bg-white rounded-lg shadow p-6 text-center">
                    <p class="text-gray-500 mb-2">No recommendations available</p>
                    <p class="text-gray-400 text-sm">Like more posts to get personalized recommendations</p>
                </div>

                <!-- Recommendations -->
                <PostComponent v-else v-for="post in recommendations" :key="post.id" :post="post" />
                
                <!-- Separator -->
                <div v-if="recommendations.length > 0 && posts.length > 0" class="my-6 border-t border-gray-200">
                    <h2 class="font-semibold text-lg mt-6 mb-4">Explore More</h2>
                </div>
            </div>
            
            <!--Users (search results) -->
            <div class="p-4 bg-[#bfdaa4] border border-gray-200 rounded-lg grid grid-cols-4 gap-4 h-72 overflow-auto"
                v-if="users.length">
                <div class="w-full min-h-64 bg-white rounded-lg shadow-md pt-6 flex flex-col items-center justify-center"
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

            <!--Posts (from search or default) -->
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
            posts: [],
            recommendations: [],
            loadingRecommendations: false,
            isSearching: false
        }
    },
    
    mounted() {
        this.getRecommendations();
        this.getDefaultPosts();
    },
    
    methods: {
        submitForm() {
            console.log('submitForm', this.query);
            this.isSearching = true;

            axios
                .post('/api/search/', {
                    query: this.query
                })
                .then(response => {
                    console.log('response:', response.data);
                    this.users = response.data.users;
                    this.posts = response.data.posts;
                })
                .catch(error => {
                    console.log('error:', error);
                });
        },
        
        getRecommendations() {
            this.loadingRecommendations = true;
            
            axios
                .get('/api/posts/item-recommendations/')
                .then(response => {
                    console.log('recommendations:', response.data);
                    this.recommendations = response.data;
                    this.loadingRecommendations = false;
                })
                .catch(error => {
                    console.log('error getting recommendations:', error);
                    this.loadingRecommendations = false;
                });
        },
    
        getDefaultPosts() {
            axios
                .get('/api/posts/')
                .then(response => {
                    // only set posts if not in search mode
                    if (!this.isSearching) {
                        this.posts = response.data;
                    }
                })
                .catch(error => {
                    console.log('error getting posts:', error);
                });
        },
        
        resetSearch() {
            this.query = '';
            this.users = [];
            this.isSearching = false;
            this.getDefaultPosts();
        }
    }
}
</script>