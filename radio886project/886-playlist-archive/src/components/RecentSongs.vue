<template>
    <div>
      <h2 class="text-xl font-bold mb-2">Letzte Songs</h2>
      <div v-if="loading">Lade...</div>
      <div v-else-if="error">{{ error }}</div>
      <ul v-else-if="recentSongs.length" class="list-disc pl-5">
        <li v-for="song in recentSongs" :key="song.id" class="mb-1">
          <button @click="selectSong(song)" class="text-left hover:text-blue-500">
            {{ formatDate(song.timestamp) }}: {{ capitalize(song.artist) }} - {{ capitalize(song.title) }}
          </button>
        </li>
      </ul>
      <div v-else>Keine kürzlich gespielten Songs verfügbar</div>
      <!-- <button @click="fetchRecentSongs" class="mt-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
        Aktualisieren
      </button> -->
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { storeToRefs } from 'pinia'
  import { useSongStore } from '../stores/songStore'
  
  const store = useSongStore()
  const { recentSongs, loading, error, songWeeklyStatsArtist, songWeeklyStatsTitle } = storeToRefs(store)
  const { fetchRecentSongs, fetchSongWeeklyStats } = store
  
  const selectedSong = ref(null)
 
  function capitalize(str) {
    return str
      .toLowerCase()
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
  }

  onMounted(() => {
    fetchRecentSongs()
  })
  
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleTimeString()
  }
  
  const selectSong = (song) => {
    selectedSong.value = song
    songWeeklyStatsArtist.value = song.artist
    songWeeklyStatsTitle.value = song.title
    fetchSongWeeklyStats() //song.title, song.artist)
  }
  </script>