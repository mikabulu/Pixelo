<template>
    <div class="flex items-center justify-center bg-gray-100">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <h1 class="text-2xl font-bold text-center mb-8">Sign Up</h1>

            <form class="space-y-6" v-on:submit.prevent="submitForm">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Name</label>
                    <input type="text" v-model="form.name"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email address</label>
                    <input type="email" v-model="form.email"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                    <input type="password" v-model="form.password1"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Repeat password</label>
                    <input type="password" v-model="form.password2"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>

            <template v-if="errors">
                <div class> <p v-for="error in errors" v-bind:key="error">{{ error }}</p></div>
            </template>

                <button
                    class="w-full bg-[#bfdaa4] text-black py-2 px-4 rounded-md hover:bg-[#a9c191] focus:outline-none focus:ring-2 focus:ring-black">
                    Sign Up
                </button>

                <p class="text-center text-sm text-gray-600">
                    Already have an account?
                    <RouterLink :to="{'name': 'login'}" class="text-black hover:text-[#bfdaa4] font-medium">Login</RouterLink>
                </p>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {useToastStore } from '../stores/toast'

export default {
    setup(){
        const toastStore = useToastStore()

        return{
            toastStore
        }
    },

    data(){
        return{
            form: {
                email: '',
                name:'',
                password1: '',
                password2: ''
            },
            errors: [],
        }
    },

    methods:{
        submitForm(){
            this.errors = []

            if (this.form.name===''){
                this.errors.push('Please input name')
            }
            if (this.form.email===''){
                this.errors.push('Please input email')
            }
            if (this.form.password1===''){
                this.errors.push('Please input password')
            }
            if (this.form.password1 !== this.form.password2){
                this.errors.push('Passwords do not match')
            }

            if (this.errors.length === 0 ){
                axios
                .post('/api/signup/', this.form)
                .then(response => {
                    if (response.data.message === 'success'){
                        this.toastStore.showToast(5000, 'Success! Please log in')

                        //resets form 
                        this.form.name=''
                        this.form.email=''
                        this.form.password1=''
                        this.form.password2=''

                    } else{
                        this.toastStore.showToast(5000, 'Something went wrong. Please try again')
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
            }
        }
    }
}
</script>