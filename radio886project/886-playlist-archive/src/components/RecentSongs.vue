<template>
    <div>
      <h2 class="text-xl font-bold mb-2">Letzte Songs</h2>
      <div v-if="loading">Lade...</div>
      <div v-else-if="error">{{ error }}</div>
      <ul v-else-if="recentSongs.length" class="list-disc pl-5">
        <li v-for="song in recentSongs" :key="song.id" class="mb-1">
          <button @click="selectSong(song)" class="text-left hover:text-blue-500">
            {{ song.artist }} - {{ song.title }} ({{ formatDate(song.timestamp) }})
          </button>
        </li>
      </ul>
      <div v-else>Keine kürzlich gespielten Songs verfügbar</div>
      <button @click="fetchRecentSongs" class="mt-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
        Aktualisieren
      </button>
  
      <div v-if="selectedSong" class="mt-4">
        <h3 class="text-lg font-semibold mb-2">{{ selectedSong.artist }} - {{ selectedSong.title }}</h3>
        <SongWeeklyChart />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { storeToRefs } from 'pinia'
  import { useSongStore } from '../stores/songStore'
  import SongWeeklyChart from './SongWeeklyChart.vue'
  
  const store = useSongStore()
  const { recentSongs, loading, error } = storeToRefs(store)
  const { fetchRecentSongs, fetchSongWeeklyStats } = store
  
  const selectedSong = ref(null)
  
  onMounted(() => {
    fetchRecentSongs()
  })
  
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }
  
  const selectSong = (song) => {
    selectedSong.value = song
    fetchSongWeeklyStats(song.title, song.artist)
  }
  </script>