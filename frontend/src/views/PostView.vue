<template>
    <div class="max-w-3xl mx-auto p-4">
        <div class="grid grid-cols-1 gap-4 mb-8" v-if="post.id">
            <!-- Posts -->
            <PostComponent v-bind:post="post" />
        </div>
        <div class="bg-white border border-gray-200 rounded-lg w-full mx-auto my-4 shadow-md">
            <form v-on:submit.prevent="submitForm" method="post">
                <div class="p-3">
                    <textarea v-model="body" class="p-2 w-full bg-gray-100 rounded-lg" placeholder="Comment"></textarea>
                </div>
                <div class="p-2 flex">
                    <button class="inline-block py-2 px-6 bg-[#bfdaa4] text-white rounded-lg">Comment</button>
                </div>
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