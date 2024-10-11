<template>
    <div>
      <h2 class="text-xl font-bold mb-2">Wie oft gespielt in den letzten Tagen?</h2>
      <form @submit.prevent="fetchStats" class="mb-4">
        <input v-model="artist" placeholder="Künstler" class="border p-2 mr-2 rounded">
        <input v-model="title" placeholder="Titel" class="border p-2 mr-2 rounded">
        <input v-model="days" type="number" placeholder="Tage" class="border p-2 mr-2 rounded" min="1">
        <button type="submit" class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded">
          Statistiken abrufen
        </button>
      </form>
      <div v-if="loading">Lade...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else-if="songStats" class="bg-gray-100 p-4 rounded-lg">
        <p><strong>{{ songStats.title }}</strong> von <strong>{{ songStats.artist }}</strong></p>
        <p>Wurde in den letzten {{ songStats.days }} Tagen {{ songStats.play_count }} mal gespielt.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { storeToRefs } from 'pinia'
  import { useSongStore } from '../stores/songStore'
  
  const store = useSongStore()
  const { songStats, loading, error } = storeToRefs(store)
  const { fetchSongStats } = store
  
  const title = ref('')
  const artist = ref('')
  const days = ref()
  
  const fetchStats = () => {
    fetchSongStats(title.value, artist.value, days.value)
  }
  </script>