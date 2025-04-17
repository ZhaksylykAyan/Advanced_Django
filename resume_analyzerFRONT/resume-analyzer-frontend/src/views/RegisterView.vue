<template>
  <div class="max-w-md mx-auto mt-20 p-6 bg-white rounded-lg shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">Register</h2>
    <form @submit.prevent="register" class="flex flex-col gap-4">
      <input v-model="username" placeholder="Username" class="input" />
      <input v-model="email" type="email" placeholder="Email" class="input" />
      <input v-model="password" type="password" placeholder="Password" class="input" />

      <select v-model="role" class="input">
        <option value="JOB_SEEKER">Job Seeker</option>
        <option value="RECRUITER">Recruiter</option>
      </select>

      <button type="submit" class="btn-primary">Register</button>
    </form>

    <p v-if="error" class="text-red-600 mt-2 text-sm text-center">{{ error }}</p>
    <p v-if="success" class="text-green-600 mt-2 text-sm text-center">{{ success }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const role = ref('JOB_SEEKER')

const error = ref('')
const success = ref('')
const router = useRouter()

async function register() {
  try {
    await api.post('users/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      role: role.value,
    })
    success.value = '✅ Registration successful! Redirecting...'
    setTimeout(() => router.push('/login'), 1500)
  } catch {
    error.value = 'Registration failed. Try again.'
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
  background-color: #10b981;
  color: white;
  padding: 0.5rem;
  border-radius: 0.375rem;
  font-weight: bold;
  cursor: pointer;
}
.btn-primary:hover {
  background-color: #059669;
}
</style>
