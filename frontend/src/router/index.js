import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'  
import HomeView from '../views/HomeView.vue'
import FeedView from '../views/FeedView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import ExploreView from '../views/ExploreView.vue'
import ProfilesView from '../views/ProfilesView.vue'

const routes = [  
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: true } //authorised access only 
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },  
  {
    path: '/signup',
    name: 'signup',
    component: SignupView,
    meta: { requiresAuth: false } 
  },
  {
    path: '/explore',
    name: 'explore',
    component: ExploreView,
    meta: { requiresAuth: true }
  },
  {
    path: '/profiles/:id',
    name: 'profiles',
    component: ProfilesView,
    meta: { requiresAuth: true }
  },
  {
    path: '/feed',
    name: 'feed',
    component: FeedView,
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
    meta: { requiresAuth: true }  
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: { name: 'login' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),  
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // if route requires auth and user is not authenticated
  if (to.meta.requiresAuth && !userStore.user.isAuthenticated) {
    next({ name: 'login' }) //if authenticated redirect to profile page 
  } else if (userStore.user.isAuthenticated && (to.name === 'login')) {
    next({ name: 'profiles', params: { id: userStore.user.id } })
  }
  else{
    next()
  }
})

export default router