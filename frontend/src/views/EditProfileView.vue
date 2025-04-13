<template>
    <div class="flex items-center justify-center bg-gray-100">
        <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
            <h1 class="text-2xl font-bold text-center mb-8">Edit Profile </h1>

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
                    <label class="block text-sm font-medium text-gray-700 mb-2">Avatar</label>
                    <label class="custom-file-upload inline-block py-2 px-2 bg-gray-600 text-white rounded-lg">
                        <input type="file" ref="file" @change="onFileChange" />
                        Upload Image
                    </label>
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
                email: this.userStore.user.email,
                name: this.userStore.user.name,
            },
            errors: []
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            if (this.form.name === '') {
                this.errors.push('Please input name')
            }
            if (this.form.email === '') {
                this.errors.push('Please input email')
            }

            if (this.errors.length === 0) {
                let formData = new FormData()
                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)
                console.log(formData)
                axios
                    .post('/api/editprofile/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'information updated') {
                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email
                            })
                            this.$router.back() //back to profile page
                        } else {
                            this.errors.push('Email already exists')
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