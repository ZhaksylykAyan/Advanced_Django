<template>
  <div class="max-w-sm mx-auto mt-20 p-6 bg-white rounded-lg shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">Login</h2>
    <form @submit.prevent="login" class="flex flex-col gap-4">
      <input v-model="username" placeholder="Username" class="input" />
      <input v-model="password" type="password" placeholder="Password" class="input" />
      <button type="submit" class="btn-primary">Login</button>
    </form>
    <p v-if="error" class="text-red-600 mt-2 text-sm text-center">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function login() {
  try {
    const res = await api.post('users/login/', {
      username: username.value,
      password: password.value,
    })
    localStorage.setItem('access_token', res.data.access)
    api.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`
    router.push('/')
  } catch {
    error.value = 'Неверный логин или пароль'
  }
}
</script>

<style scoped>
.input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
}
.btn-primary {
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem;
  border-radius: 0.375rem;
  font-weight: bold;
  cursor: pointer;
}
.btn-primary:hover {
  background-color: #2563eb;
}
</style>
