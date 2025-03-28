<template>
    <div class="flex items-center justify-center bg-gray-100">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <h1 class="text-2xl font-bold text-center mb-8">Change your Password</h1>

            <form class="space-y-6" v-on:submit.prevent="submitForm">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Your Old Password</label>
                    <input type="password" v-model="form.old_password"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Your New Password</label>
                    <input type="password" v-model="form.new_password1"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Repeat Password</label>
                    <input type="password" v-model="form.new_password2"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                </div>

                <!-- Error display section -->
                <div v-if="errors.length" class="bg-red-50 text-red-500 p-3 rounded-md">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <button
                    class="w-full bg-[#bfdaa4] text-black py-2 px-4 rounded-md hover:bg-[#a9c191] focus:outline-none focus:ring-2 focus:ring-black">
                    Save Changes
                </button>
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
                old_password: '',
                new_password1: '',
                new_password2: ''
            },
            errors: []
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('old_password', this.form.old_password)
                formData.append('new_password1', this.form.new_password1)
                formData.append('new_password2', this.form.new_password2)
                console.log(formData)
                axios
                    .post('/api/editpassword/', formData,{
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'password updated') {
                            this.$router.push(`/profile/${this.userStore.user.id}`) //back to profile page
                        } else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data) {
                                this.errors.push(data[key][0].message)
                            }
                        }
                    })
                    .catch(error => {
                        console.log(error)
                    })
            }
        }
    }
}

</script>