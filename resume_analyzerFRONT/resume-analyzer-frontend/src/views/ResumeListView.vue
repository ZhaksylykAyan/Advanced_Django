<template>
  <div class="max-w-4xl mx-auto mt-20 p-6">
    <h2 class="text-2xl font-bold mb-6 text-center">📂 My Uploaded Resumes</h2>

    <div v-if="resumes.length === 0" class="text-center text-gray-500">
      You haven't uploaded any resumes yet.
    </div>

    <div
      v-for="resume in resumes"
      :key="resume.id"
      class="bg-white p-4 rounded-lg shadow mb-6"
    >
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-semibold">📄 {{ resume.file.split('/').pop() }}</h3>
        <span class="text-sm text-gray-500">{{ new Date(resume.uploaded_at).toLocaleString() }}</span>
      </div>

      <div v-if="resume.parsed_data" class="mt-4">
        <p><strong>Skills:</strong> {{ resume.parsed_data.skills.join(', ') }}</p>

        <div class="mt-2">
          <p class="font-medium">Experience:</p>
          <ul class="list-disc pl-5 text-sm text-gray-700">
            <li v-for="(exp, i) in resume.parsed_data.experience" :key="i">{{ exp }}</li>
          </ul>
        </div>

        <div class="mt-2">
          <p class="font-medium">Education:</p>
          <ul class="list-disc pl-5 text-sm text-gray-700">
            <li v-for="(edu, i) in resume.parsed_data.education" :key="i">{{ edu }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const resumes = ref([])
const token = localStorage.getItem('access_token')

onMounted(async () => {
  const res = await api.get('resumes/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
  resumes.value = res.data
})
</script>
