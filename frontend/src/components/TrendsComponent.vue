<template>
    <div class="flex flex-row items-center bg-white rounded-full shadow-md px-4 py-2 overflow-x-auto">
        <p class="mr-5">What's trending?</p>
        <div v-for="trend in trends" v-bind:key="trend.id" class="flex items-center m-2">
            <RouterLink :to="{name:'hashtagview', params:{id: trend.hashtag}}"><strong>{{ trend.hashtag }}</strong></RouterLink>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'TrendsComponent',
    data() {
        return {
            trends: []
        }
    },
    mounted() {
        this.getTrends()
    },

    methods: {
        getTrends() {
            axios
                .get('/api/posts/trends/')
                .then(response => {
                    console.log('response:', response.data)
                    this.trends = response.data
                })
                .catch(error => {
                    console.log('error:', error)
                })
        }
    },
}

</script>