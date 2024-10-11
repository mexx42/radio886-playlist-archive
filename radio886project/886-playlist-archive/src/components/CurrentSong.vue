<template>
    <div>
      <h2 class="text-xl font-bold mb-2">Aktueller Song</h2>
      <div v-if="loading">Lade...</div>
      <div v-else-if="error">{{ error }}</div>
      <div v-else-if="currentSong" class="bg-gray-100 p-4 rounded-lg">
        <p class="font-semibold">{{ capitalize(currentSong.artist) }} - {{ capitalize(currentSong.title) }}</p>
      </div>
      <div v-else>Kein aktueller Song verfügbar</div>
      <!-- <button @click="fetchCurrentSong" class="mt-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
        Aktualisieren
      </button> -->
    </div>
  </template>
  
  <script setup>
  import { onMounted } from 'vue'
  import { storeToRefs } from 'pinia'
  import { useSongStore } from '../stores/songStore'
  
  const store = useSongStore()
  const { currentSong, loading, error } = storeToRefs(store)
  const { fetchCurrentSong } = store
  
  function capitalize(str) {
    return str
      .toLowerCase()
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  onMounted(() => {
    fetchCurrentSong()
  })
  </script>