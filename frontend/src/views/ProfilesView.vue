<template>
    <!-- Main Container -->
    <div class="max-w-3xl mx-auto p-4">
        <div class="grid grid-cols-1 gap-4">

            <!-- Profile Container -->
            <div class="w-full min-h-64 bg-white rounded-lg shadow-md pt-6 relative"> <!-- 'relative' for positioning -->
                <!-- settings -->
                <div v-if="userStore.user.id === user.id" class="absolute top-4 left-4 settings-menu-container">
                    <div class="relative">
                        <div @click.stop="toggleSettingsMenu" class="cursor-pointer">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>
                        </div>

                        <!-- Dropdown Menu -->
                        <div v-if="showSettingsMenu" ref="settingsMenu" @click.stop
                            class="absolute left-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
                            <RouterLink to="/profile/edit"
                                class="block px-4 py-2 text-sm text-gray-700 hover:bg-[#e8f2d7] cursor-pointer">
                                Edit Profile
                            </RouterLink>
                            <RouterLink to="/profile/editpassword"
                                class="block px-4 py-2 text-sm text-gray-700 hover:bg-[#e8f2d7] cursor-pointer">
                                Change Password
                            </RouterLink>
                            <div @click="logout"
                                class="block px-4 py-2 text-sm text-gray-700 hover:bg-[#e8f2d7] cursor-pointer">
                                Logout
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Follow button (other users) -->
                <button v-if="userStore.user.id !== user.id"
                    :class="isFollowing ? 'bg-gray-300 hover:bg-gray-400' : 'bg-[#bfdaa4] hover:bg-[#a9c191]'"
                    class="absolute top-4 right-4 text-black py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-black"
                    @click="toggleFollow">
                    {{ isFollowing ? 'Unfollow' : 'Follow' }}
                </button>

                <!-- Add Post (self)-->
                <button v-if="userStore.user.id === user.id" @click="showAddPostModal = true"
                    class="absolute top-4 right-4 bg-[#bfdaa4] text-black py-2 px-4 rounded-md hover:bg-[#a9c191] focus:outline-none focus:ring-2 focus:ring-black">
                    Add Post
                </button>

                <div class="flex flex-col items-center justify-center">
                    <img :src="user.get_avatar" class="h-40 w-40 mb-3 rounded-full object-cover">
                    <p><strong>{{ user.name }}</strong></p>
                    <div class="mt-3 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ followers_count }} {{ followers_count === 1 ? 'follower' :
                            'followers' }}</p>
                        <p class="text-xs text-gray-500">{{ following_count }} following</p>
                        <p class="text-xs text-gray-500">{{ posts.length }} {{ posts.length === 1 ? 'post' : 'posts' }}</p>
                    </div>
                    <p class="text-xs text-500 mt-4">Biography</p>

                    <ul
                        class="flex flex-wrap text-sm font-medium text-center text-gray-500 dark:border-gray-700 dark:text-gray-400 mt-5">
                        <li class="me-2">
                            <a href="#" aria-current="page"
                                class="inline-block p-4 text-[#a9c191] rounded-t-lg dark:text-blue-500">Feed</a>
                        </li>
                        <li class="me-2">
                            <a href="#"
                                class="inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50 dark:hover:bg-[#bfdaa4] dark:hover:text-gray-300">Gallery</a>
                        </li>
                        <li class="me-2">
                            <a href="#"
                                class="inline-block p-4 rounded-t-lg hover:text-gray-600 hover:bg-gray-50 dark:hover:bg-[#bfdaa4] dark:hover:text-gray-300">Portfolio</a>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Posts  -->
            <PostComponent v-for="post in posts" :key="post.id" :post="post" @postDeleted="deletePost"/>
        </div>
    </div>

    <!-- Add Post Modal -->
    <div v-if="showAddPostModal" class="fixed inset-0 backdrop-blur-xs flex items-center justify-center z-50">
        <div class="bg-white border border-gray-200 rounded-lg max-w-lg w-full mx-4">
            <div class="flex justify-between items-center p-4 border-b">
                <h3 class="font-semibold">Add Post</h3>
                <button @click="showAddPostModal = false" class="text-gray-500 hover:text-gray-700">✕</button>
            </div>
            <form v-on:submit.prevent="submitFormAndClose" method="post">
                <div id="preview" v-if="url" class="mx-5 mt-5">
                    <img :src="url" />
                </div>
                <div class="p-4">
                    <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Add Post"></textarea>
                </div>
                <div class="p-4 border-t border-gray-100 flex justify-between">
                    <label class="custom-file-upload inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                        <input type="file" ref="file" @change="onFileChange" />
                        Upload Image
                    </label>
                    <button class="inline-block py-4 px-6 bg-[#bfdaa4]  text-white rounded-lg">Post</button>
                </div>
            </form>
        </div>
    </div>
</template>

<style>
input[type="file"] {
    display: none;
}
</style>
  
<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import PostComponent from '@/components/PostComponent.vue'
export default {
    name: 'GridLayout',

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
            posts: [],
            user: {},
            body: '',
            showAddPostModal: false,
            isFollowing: false,
            followers_count: 0,
            following_count: 0,
            showSettingsMenu: false,
            url: null
        }
    },
    watch: {
        //observes changes to user ID and refreshes component
        '$route.params.id': {
            handler(newId) {
                this.getFeed();
                this.checkFollowStatus();
            },
            immediate: true
        }
    },
    mounted() {
        this.getFeed()
        this.checkFollowStatus();
        document.addEventListener('click', this.closeSettingsMenuOutside); //close menu when click outside
    },
    beforeUnmount() {
        document.removeEventListener('click', this.closeSettingsMenuOutside);
    },
    methods: {
        deletePost(id){
            this.posts = this.posts.filter(post => post.id !== id)
        },
        onFileChange(e) {
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },
        logout() {
            axios
                .post('/api/logout/')
                .then(response => {
                    this.userStore.removeToken();
                    this.$router.push('/login');
                })
                .catch(error => {
                    console.log('Error logging out:', error)
                });
        },
        toggleSettingsMenu() {
            this.showSettingsMenu = !this.showSettingsMenu;
        },
        //close settings menu when click outside
        closeSettingsMenuOutside(event) {
            if (this.$refs.settingsMenu && !this.$refs.settingsMenu.contains(event.target)) {
                this.showSettingsMenu = false;
            }
        },
        getFeed() {
            axios
                .get(`/api/posts/profiles/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data.posts
                    this.user = response.data.user
                    this.getFollowerStats();
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        getFollowerStats() {
            axios
                .get(`/api/followers/stats/${this.$route.params.id}/`)
                .then(response => {
                    this.followers_count = response.data.followers_count;
                    this.following_count = response.data.following_count;
                })
                .catch(error => {
                    console.log('Error getting follower stats', error);
                });
        },

        checkFollowStatus() {
            //only check if viewing other users profile
            if (!this.userStore.user.id || this.userStore.user.id === this.$route.params.id) {
                return;
            }

            axios
                .get(`/api/followers/check/${this.$route.params.id}/`)
                .then(response => {
                    this.isFollowing = response.data.is_following;
                })
                .catch(error => {
                    console.log('Error checking follow status:', error);
                });
        },

        toggleFollow() {
            if (this.isFollowing) {
                //unfollow
                axios
                    .post(`/api/followers/unfollow/${this.$route.params.id}/`)
                    .then(response => {
                        this.isFollowing = false;
                        this.followers_count -= 1;
                    })
                    .catch(error => {
                        console.log('Error unfollowing:', error)
                    });
            } else {
                //follow
                axios
                    .post(`/api/followers/follow/${this.$route.params.id}/`)
                    .then(response => {
                        this.isFollowing = true;
                        this.followers_count += 1;
                    })
                    .catch(error => {
                        console.log('Error following', error);
                    });
            }
        },

        submitForm() {
            console.log('submitForm', this.body)
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                })
                .then(response => {
                    console.log('data', response.data)
                    this.posts.unshift(response.data)
                    this.body = ''
                    this.url=null
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitFormAndClose() {
            this.submitForm()
            this.showAddPostModal = false
        }
    }

}
</script>
  

<style scoped></style>