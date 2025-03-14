<template>
    <!-- Main Container -->
    <div class="max-w-3xl mx-auto p-4">
        <div class="grid grid-cols-1 gap-4">
            <!-- Profile Container -->
            <div class="w-full min-h-64 bg-white rounded-lg shadow-md pt-6 flex flex-col items-center justify-center">
                <img src="../assets/charlie.jpg" class="h-40 w-40 mb-3 rounded-full object-cover">
                <p><strong>Charlie</strong></p>
                <div class="mt-3 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">X friends</p>
                    <p class="text-xs text-gray-500">X posts</p>
                </div>
                <p class="text-xs text-500 mt-4">Biography</p>
                <button
                    @click="showAddPostModal = true"
                    class="bg-[#bfdaa4] text-black py-2 px-4 mt-4 rounded-md hover:bg-[#a9c191] focus:outline-none focus:ring-2 focus:ring-black">
                    Add Post
                </button>
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

            <!-- Post Container -->
            <div class="w-full aspect-square bg-white rounded-lg shadow-md p-4 flex flex-col" v-for="post in posts"
                v-bind:key="post.id">
                <!-- Header -->
                <div class="mb-6 flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                        <img src="../assets/charlie.jpg" class="w-[40px] rounded-full">

                        <p><strong>{{ post.created_by.name }}</strong></p>
                    </div>
                    <p class="text-gray-600">{{ post.created_at_formatted }} ago</p>
                </div>

                <!-- Posts  -->
                <p>{{ post.body }}</p>


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

                            <span class="text-gray-500 text-xs">X likes</span>
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

    <!-- Add Post Modal -->
    <div v-if="showAddPostModal" class="fixed inset-0 backdrop-blur-xs flex items-center justify-center z-50">
        <div class="bg-white border border-gray-200 rounded-lg max-w-lg w-full mx-4">
            <div class="flex justify-between items-center p-4 border-b">
                <h3 class="font-semibold">Add Post</h3>
                <button @click="showAddPostModal = false" class="text-gray-500 hover:text-gray-700">✕</button>
            </div>
            <form v-on:submit.prevent="submitFormAndClose" method="post">
                <div class="p-4">
                    <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Add Post"></textarea>
                </div>

                <div class="p-4 border-t border-gray-100 flex justify-between">
                    <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                    <button class="inline-block py-4 px-6 bg-[#bfdaa4]  text-white rounded-lg">Post</button>
                </div>
            </form>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios'
export default {
    name: 'GridLayout',

    data() {
        return {
            posts: [],
            body: '',
            showAddPostModal: false,
        }
    },


    mounted() {
        this.getFeed()
    },
    methods: {
        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            console.log('submitForm', this.body)

            axios
            .post('/api/posts/create/', {
                'body': this.body
            })
            .then(response => {
                console.log('data', response.data)
                this.posts.unshift(response.data)
                this.body=''
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