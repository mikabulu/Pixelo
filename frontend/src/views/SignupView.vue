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
                <!-- Account Type Dropdown -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Account Type</label>
                    <select v-model="form.account_type"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#bfdaa4]">
                        <option disabled value="">Please select one</option>
                        <option value="hobbyist">Hobbyist</option>
                        <option value="professional">Professional</option>
                        <option value="student">Student</option>
                        <option value="studio">Studio</option>
                        <option value="other">Other</option>
                    </select>
                </div>

                <!-- Error display section -->
                <div v-if="errors.length" class="bg-red-50 text-red-500 p-3 rounded-md">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <button
                    class="w-full bg-[#bfdaa4] text-black py-2 px-4 rounded-md hover:bg-[#a9c191] focus:outline-none focus:ring-2 focus:ring-black">
                    Sign Up
                </button>

                <p class="text-center text-sm text-gray-600">
                    Already have an account?
                    <RouterLink :to="{ 'name': 'login' }" class="text-black hover:text-[#bfdaa4] font-medium">Login
                    </RouterLink>
                </p>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            form: {
                email: '',
                name: '',
                password1: '',
                password2: '',
                account_type: ''
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
            if (this.form.password1 === '') {
                this.errors.push('Please input password')
            }
            if (this.form.password1 !== this.form.password2) {
                this.errors.push('Passwords do not match')
            }
            if (this.form.account_type === '') {
                this.errors.push('Please select an account type')
            }


            if (this.errors.length === 0) {
                axios
                    .post('/api/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'success') {
                            //resets form 
                            this.form.name = ''
                            this.form.email = ''
                            this.form.password1 = ''
                            this.form.password2 = ''

                            this.$router.push({ name: 'login' })
                        } else {
                            if (response.data.errors) {
                                // process each field's errors
                                for (const field in response.data.errors) {
                                    const errors = response.data.errors[field];
                                    // returns arrays of errors for each field
                                    errors.forEach(error => {
                                        this.errors.push(error);
                                    });
                                }
                            } else {
                                this.errors.push('Something went wrong. Please try again')
                            }
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                        this.errors.push('An error occurred during signup')
                    })
            }
        }
    }
}
</script>