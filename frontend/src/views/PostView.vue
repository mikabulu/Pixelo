<template>
    <div class="max-w-3xl mx-auto p-4">
        <div class="grid grid-cols-1 gap-4 mb-8" v-if="post.id">
            <!-- Posts -->
            <PostComponent v-bind:post="post" />
        </div>
        <!-- Add Comment box -->
        <div class="bg-white border border-gray-200 rounded-lg w-full mx-auto my-4 shadow-md p-3">
            <form v-on:submit.prevent="submitForm" method="post" class="flex items-start gap-2">
                <textarea v-model="body" class="p-2 flex-grow bg-gray-100 rounded-lg resize-none h-10"
                    placeholder="Add a comment"></textarea>
                <button type="submit" :disabled="!body.trim()"
                    class="py-2 px-4 bg-[#bfdaa4] text-white rounded-lg flex items-center justify-center h-10 disabled:opacity-50">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 0 1-.923 1.785A5.969 5.969 0 0 0 6 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337Z" />
                    </svg>
                </button>
            </form>
        </div>

        <div class="bg-white border border-gray-200 rounded-lg mb-2" v-for="comment in post.comments"
            v-bind:key="comment.id">
            <CommentComponent v-bind:comment="comment" />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import PostComponent from '@/components/PostComponent.vue'
import CommentComponent from '@/components/CommentComponent.vue'

export default {
    name: 'PostView',

    components: {
        PostComponent,
        CommentComponent
    },

    setup() {
        const userStore = useUserStore()
        return { userStore }
    },

    data() {
        return {
            post: {
                id: null,
                comments: []
            },
            body: ''
        }
    },

    mounted() {
        this.getPost()
    },

    methods: {
        getPost() {
            axios
                .get(`/api/posts/${this.$route.params.id}/`)
                .then(response => {
                    this.post = response.data.post
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        submitForm() {
            console.log('submitForm', this.body)

            axios
                .post(`/api/posts/${this.$route.params.id}/comment/`, {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)
                    this.post.comments.push(response.data)
                    this.post.comments_count += 1 //updates comments count immediately 
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>