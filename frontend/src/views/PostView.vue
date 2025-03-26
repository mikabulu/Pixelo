<template>
    <div class="max-w-3xl mx-auto p-4">
        <div class="bg-white border border-gray-200 rounded-lg max-w-lg w-full mx-auto my-4 shadow-md">
            <div class="flex justify-between items-center p-4 border-b">
                <h3 class="font-semibold">Add Comment</h3>
            </div>
            <form v-on:submit.prevent="submitForm" method="post">
                <div class="p-4">
                    <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Add Comment"></textarea>
                </div>

                <div class="p-4 border-t border-gray-100 flex justify-between">

                    <button class="inline-block py-4 px-6 bg-[#bfdaa4] text-white rounded-lg">Comment</button>
                </div>
            </form>
        </div>
        <div class="grid grid-cols-1 gap-4 mb-8" v-if="post.id">
            <!-- Posts -->
            <PostComponent v-bind:post="post" />
        </div>
        <div class="bg-white border border-gray-200 rounded-lg mb-2" v-for="comment in post.comments" v-bind:key="comment.id">
        <CommentComponent v-bind:comment="comment"/></div>
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