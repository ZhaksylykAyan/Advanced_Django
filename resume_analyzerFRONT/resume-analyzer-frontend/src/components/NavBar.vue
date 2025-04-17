<template>
  <nav class="bg-gray-800 text-white py-4 shadow">
    <div class="max-w-6xl mx-auto px-4 flex justify-between items-center">
      <div class="flex gap-4 items-center">
        <router-link to="/" class="text-sm hover:text-blue-400 transition">Upload</router-link>
        <router-link to="/resumes" class="text-sm hover:text-blue-400 transition">My Resumes</router-link>
        <router-link to="/jobs" class="text-sm hover:text-blue-400 transition">Jobs</router-link>
      </div>

      <div class="flex items-center gap-4">
        <template v-if="!isAuthenticated">
          <router-link to="/login" class="text-sm hover:text-blue-400 transition">Login</router-link>
          <router-link to="/register" class="text-sm hover:text-blue-400 transition">Register</router-link>
        </template>
        <template v-else>
          <button @click="logout" class="text-sm bg-red-500 px-3 py-1 rounded hover:bg-red-600 transition">
            Logout
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isAuthenticated = computed(() => {
  return !!localStorage.getItem('access_token')
})

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
}
</script>

<style scoped>

</style>
