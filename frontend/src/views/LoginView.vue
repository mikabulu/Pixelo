<template>
    <div class="flex items-center justify-center bg-gray-100">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <img src="../assets/logo.png" class="block mx-auto mb-6 h-60">
            <h1 class="text-2xl font-bold text-center mb-8">Sign in to Pixelo</h1>

            <form class="space-y-6" v-on:submit.prevent="submitForm">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email address</label>
                    <input type="email" v-model="form.email"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Password</label>
                    <input type="password" v-model="form.password"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>

                <!-- Error display section -->
                <div v-if="errors.length" class="bg-red-50 text-red-500 p-3 rounded-md">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <button
                    class="w-full bg-[#bfdaa4] text-black py-2 px-4 rounded-md hover:bg-[#a9c191] focus:outline-none focus:ring-2 focus:ring-black">
                    Sign in
                </button>

                <p class="text-center text-sm text-gray-600">
                    Don't have an account?
                    <RouterLink :to="{ 'name': 'signup' }" class="text-black hover:text-[#bfdaa4] font-medium">Sign up
                    </RouterLink>
                </p>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
export default {
    setup() {
        const userStore = useUserStore()
        return {
            userStore
        }
    },
    data() {
        return {
            form: {
                email: '',
                password: '',
            },
            errors: []
        }
    },
    methods: {
        async submitForm() {
            this.errors = []
            if (this.form.email === '') {
                this.errors.push('Please input email')
            }
            if (this.form.password === '') {
                this.errors.push('Please input password')
            }

            if (this.errors.length === 0) {
                await axios
                    .post('/api/login/', this.form)
                    .then(response => {
                        this.userStore.setToken(response.data)
                        axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                    })
                    .catch(error => {
                        console.log('error', error)
                        this.errors.push('Invalid email or password')
                    })

                await axios
                    .get('/api/me/')
                    .then(response => {
                        this.userStore.setUserInfo(response.data)
                        this.$router.push({
                            name: 'profiles',
                            params: { id: this.userStore.user.id }
                        })
                    })
                    .catch(error => {
                        console.log('error', error)
                    })


            }

        }
    }
}
</script>