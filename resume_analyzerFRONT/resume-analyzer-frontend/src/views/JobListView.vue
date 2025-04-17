<template>
  <div class="max-w-5xl mx-auto mt-20 p-6">
    <h2 class="text-2xl font-bold mb-6 text-center">💼 My Job Listings</h2>

    <!-- Создание вакансии -->
    <form @submit.prevent="createJob" class="bg-white p-6 rounded-lg shadow mb-10 space-y-4">
      <h3 class="text-xl font-semibold mb-2">📝 Create New Job</h3>
      <input v-model="title" placeholder="Job Title" class="w-full p-2 border border-gray-300 rounded" />
      <input v-model="location" placeholder="Location" class="w-full p-2 border border-gray-300 rounded" />
      <textarea v-model="description" placeholder="Job Description" class="input h-24" />
      <input v-model="skills" placeholder="Required Skills (comma-separated)" class="w-full p-2 border border-gray-300 rounded" />
      <button type="submit" class="bg-blue-600 text-white font-bold py-2 px-4 rounded hover:bg-blue-700 w-full">Create Job</button>
    </form>

    <!-- Список вакансий -->
    <div
      v-for="job in jobs"
      :key="job.id"
      class="bg-white p-6 rounded-lg shadow mb-6"
    >
      <h3 class="text-lg font-bold">{{ job.title }}</h3>
      <p class="text-gray-600">{{ job.description }}</p>
      <p class="text-sm mt-1"><strong>Location:</strong> {{ job.location }}</p>
      <p class="text-sm"><strong>Skills:</strong> {{ job.required_skills.join(', ') }}</p>

      <button @click="getMatches(job.id)" class="bg-green-600 text-white font-bold py-2 px-4 rounded hover:bg-green-700 mt-4">
        🔍 View Matching Resumes
      </button>

      <!-- Матчинг -->
      <div v-if="job.matches" class="mt-4">
        <h4 class="font-semibold mb-2">Matching Resumes:</h4>
        <ul class="list-disc pl-5 text-sm">
          <li
            v-for="match in job.matches"
            :key="match.resume_id"
          >
            <span class="font-medium">{{ match.username }}</span>
            — {{ match.score }}% match ({{ match.skills_matched.join(', ') }})
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const title = ref('')
const location = ref('')
const description = ref('')
const skills = ref('')
const jobs = ref([])

const token = localStorage.getItem('access_token')

const headers = {
  Authorization: `Bearer ${token}`,
}

async function fetchJobs() {
  const res = await api.get('jobs/', { headers })
  jobs.value = res.data
}

async function createJob() {
  const payload = {
    title: title.value,
    location: location.value,
    description: description.value,
    required_skills: skills.value.split(',').map(s => s.trim()),
  }

  await api.post('jobs/', payload, { headers })
  await fetchJobs()
}

async function getMatches(jobId) {
  const res = await api.get(`jobs/${jobId}/match_resumes/`, { headers })
  const job = jobs.value.find(j => j.id === jobId)
  job.matches = res.data
}

onMounted(fetchJobs)
</script>

<style scoped>

</style>
