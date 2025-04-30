<template>
  <div class="max-w-xl mx-auto mt-20 p-6 bg-white rounded-lg shadow">
    <h2 class="text-2xl font-bold mb-4 text-center">📄 Upload Resume</h2>

    <input type="file" @change="onFileChange" class="file-input mb-4" />

    <button @click="uploadResume" class="btn-primary w-full">
      Upload
    </button>

    <div v-if="response" class="mt-6">
      <h3 class="text-xl font-semibold mb-2">🧠 Parsed Resume:</h3>

      <div class="bg-gray-100 p-4 rounded">
        <p><strong>Skills:</strong> {{ response.skills?.join(', ') }}</p>
        <p class="mt-2"><strong>Experience:</strong></p>
        <ul class="list-disc pl-5">
          <li v-for="(exp, i) in response.experience" :key="i">{{ exp }}</li>
        </ul>

        <p class="mt-2"><strong>Education:</strong></p>
        <ul class="list-disc pl-5">
          <li v-for="(edu, i) in response.education" :key="i">{{ edu }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const file = ref(null)
const response = ref(null)

function onFileChange(e) {
  file.value = e.target.files[0]
}

async function uploadResume() {
  if (!file.value) return alert('Please select a file first')

  const formData = new FormData()
  formData.append('file', file.value)

  const token = localStorage.getItem('access_token')
  const res = await api.post('resumes/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      Authorization: `Bearer ${token}`,
    },
  })

  response.value = res.data.parsed_data
}
</script>

<style scoped>
.file-input {
  display: block;
  width: 100%;
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
