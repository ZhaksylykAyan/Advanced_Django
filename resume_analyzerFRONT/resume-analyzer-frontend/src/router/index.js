import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ResumeUploadView from '../views/ResumeUploadView.vue'
import ResumeListView from '../views/ResumeListView.vue'
import JobListView from '../views/JobListView.vue'

const routes = [
  { path: '/', name: 'Upload', component: ResumeUploadView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/resumes', name: 'Resumes', component: ResumeListView },
  { path: '/jobs', name: 'Jobs', component: JobListView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register']
  const authRequired = !publicPages.includes(to.path)
  const token = localStorage.getItem('access_token')

  if (authRequired && !token) {
    return next('/login')
  }
  next()
})

export default router
