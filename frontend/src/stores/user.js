import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
    state: () => ({
        user: {
            isAuthenticated: false,
            id: null,
            name: null,
            email: null,
            access: null,
            refresh: null,
            avatar: null,
            bio: null,
            account_type: 'enthusiast',
        }
    }),

    actions: {
        initStore() {
            console.log('initStore', localStorage.getItem('user.access'))

            if (localStorage.getItem('user.access')) {
                console.log('User has access!')

                this.user.access = localStorage.getItem('user.access')
                this.user.refresh = localStorage.getItem('user.refresh')
                this.user.id = localStorage.getItem('user.id')
                this.user.name = localStorage.getItem('user.name')
                this.user.email = localStorage.getItem('user.email')
                this.user.avatar = localStorage.getItem('user.avatar')
                this.user.bio = localStorage.getItem('user.bio')
                this.user.account_type = localStorage.getItem('user.account_type')
                this.user.isAuthenticated = true

                this.refreshToken()

                console.log('Initialized user:', this.user)
            }
        },

        setToken(data) {
            console.log('setToken', data)

            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', data.access)
            localStorage.setItem('user.refresh', data.refresh)

            console.log('user.access: ', localStorage.getItem('user.access'))
        },

        removeToken() {
            console.log('removeToken')

            this.user.refresh = null
            this.user.access = null
            this.user.isAuthenticated = false
            this.user.id = null
            this.user.name = null
            this.user.email = null
            this.user.avatar = null
            this.user.bio = null
            this.user.account_type = null

            localStorage.setItem('user.access', '')
            localStorage.setItem('user.refresh', '')
            localStorage.setItem('user.id', '')
            localStorage.setItem('user.name', '')
            localStorage.setItem('user.email', '')
            localStorage.setItem('user.avatar', '')
            localStorage.setItem('user.bio', '')
            localStorage.setItem('user.account_type', '')
        },

        setUserInfo(user) {
            console.log('setUserInfo', user)

            this.user.id = user.id
            this.user.name = user.name
            this.user.email = user.email
            this.user.avatar = user.avatar
            this.user.bio = user.bio
            this.user.account_type = user.account_type

            localStorage.setItem('user.id', this.user.id)
            localStorage.setItem('user.name', this.user.name)
            localStorage.setItem('user.email', this.user.email)
            localStorage.setItem('user.avatar', this.user.avatar)
            localStorage.setItem('user.bio', this.user.bio)
            localStorage.setItem('user.account_type', this.user.account_type)

            console.log('User', this.user)
        },


        refreshToken() {
            axios.post('/api/refresh/', {
                refresh: this.user.refresh
            })
                .then((response) => {
                    this.user.access = response.data.access

                    localStorage.setItem('user.access', response.data.access)

                    axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                })
                .catch((error)=>{
                    console.log(error)

                    this.removeToken()
                })
        },
    }
})