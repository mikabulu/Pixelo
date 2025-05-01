<template>
    <div class="max-w-7xl mx-auto flex justify-center">
        <div class="w-full max-w-4xl space-y-4">
            <!--Search Bar -->
            <div class="bg-white border border-gray-200 rounded-full">
                <form v-on:submit.prevent="submitForm" class="p-2 flex space-x-4 rounded-full">
                    <input v-model="query" type="search" placeholder="Search for artists or posts"
                        class="p-3 w-full bg-gray-100 rounded-full">
                    <button class="inline-block py-4 px-6 bg-[#bfdaa4] text-black rounded-full"><svg
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                        </svg>
                    </button>
                </form>
            </div>


            <!-- Recommendations Section (when not searching) -->
            <div v-if="!isSearching" class="w-full">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="font-semibold text-lg">Recommended For You</h2>
                </div>

                <!-- No recommendations message -->
                <div v-if="recommendations.length === 0" class="bg-white rounded-lg shadow p-6 text-center">
                    <p class="text-gray-500 mb-2">No recommendations available</p>
                    <p class="text-gray-400 text-sm">Like more posts to get personalised recommendations</p>
                </div>

                <!-- Recommendations -->
                <PostComponent v-else v-for="post in recommendations" :key="post.id" :post="post" class="mb-4" />

                <!-- Separator -->
                <div class="my-6 border-t border-gray-200">
                    <h2 class="font-semibold text-lg mt-6 mb-4">Explore More</h2>
                </div>
            </div>

            <!--Users (search results) -->
            <div class="p-4 bg-[#bfdaa4] border border-gray-200 rounded-lg grid grid-cols-4 gap-4 h-72 overflow-auto"
                v-if="users.length">
                <div class="w-full min-h-64 bg-white rounded-lg shadow-md pt-6 flex flex-col items-center justify-center card"
                    v-for="user in users" v-bind:key="user.id">
                    <img :src="user.get_avatar" class=" avatar h-40 w-40 mb-3 rounded-full object-cover">
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

            <!--Posts (from search or explore) -->
            <PostComponent v-for="post in posts" :key="post.id" :post="post" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import PostComponent from '@/components/PostComponent.vue'
import { useUserStore } from '@/stores/user'

export default {
    name: 'ExploreView',

    components: {
        PostComponent
    },
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            query: '',
            users: [],
            posts: [],
            recommendations: [],
            isSearching: false,
            followingIds: []
        }
    },
    mounted() {
        this.getFollowingList();
        this.getRecommendations();
        this.getExplorePosts();
    },
    methods: {
        getFollowingList() {
            axios
                .get(`/api/following/list/${this.userStore.user.id}/`)
                .then(response => {
                    // get just IDs 
                    this.followingIds = response.data.map(user => user.id);
                })
                .catch(error => {
                    console.log('Error fetching following list:', error);
                });
        },
        submitForm() {
            this.isSearching = true;

            axios
                .post('/api/search/', {
                    query: this.query
                })
                .then(response => {
                    this.users = response.data.users;
                    this.posts = response.data.posts;
                })
                .catch(error => {
                    console.log('error:', error);
                });
        },
        getRecommendations() {

            axios
                .get('/api/posts/recommendations/')
                .then(response => {
                    // filter recommendations posts from self and users followed
                    this.recommendations = response.data.filter(post =>
                        post.created_by.id !== this.userStore.user.id &&
                        !this.followingIds.includes(post.created_by.id)
                    );
                })
                .catch(error => {
                    console.log('error getting recommendations:', error);
                });
        },
        getExplorePosts() {
            axios
                .get('/api/posts/')
                .then(response => {
                    if (!this.isSearching) {
                        // filter explore posts from self and users followed
                        this.posts = response.data.filter(post =>
                            post.created_by.id !== this.userStore.user.id &&
                            !this.followingIds.includes(post.created_by.id)
                        );
                    }
                })
                .catch(error => {
                    console.log('Error getting posts:', error);
                });
        },
        resetSearch() {
            this.query = '';
            this.users = [];
            this.isSearching = false;
            this.getExplorePosts();
        }
    }
}
</script>

<style scoped>
@media screen and (max-width: 800px) {
    .grid-cols-4 {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .p-4 {
        padding: 0.5rem;
    }

    .gap-4 {
        gap: 0.5rem;
    }


    .avatar {
        height: 6rem;
        width: 6rem;
    }

    .text-xs {
        font-size: 0.65rem;
    }


}
</style>