import { defineStore } from 'pinia'
import axios from 'axios'
import ReconnectingWebSocket from 'reconnecting-websocket'

const API_BASE_URL = 'http://localhost:8000';

export const useSongStore = defineStore('song', {
  state: () => ({
    currentSong: null,
    recentSongs: [],
    songStats: null,
    songWeeklyStats: null,
    songWeeklyStatsArtist: null,
    songWeeklyStatsTitle: null,
    loading: false,
    error: null,
    socket: null
  }),
  actions: {
    initializeSocket() {
      this.socket = new ReconnectingWebSocket('ws://localhost:8000/ws/songs/')

      this.socket.addEventListener('open', () => {
        console.log('Verbunden mit WebSocket')
      })

      this.socket.addEventListener('message', (event) => {
        const data = JSON.parse(event.data)
        console.log (data)
        if (data.message.type === 'new_song') {
          this.handleNewSong(data.message.song)
        }
      })

      this.socket.addEventListener('close', () => {
        console.log('Verbindung geschlossen. Versuche erneut zu verbinden...')
      })

      this.socket.addEventListener('error', (error) => {
        console.error('WebSocket Fehler:', error)
      })
    },
    handleNewSong(song) {
      this.currentSong = song
      this.recentSongs.unshift(song)
      if (this.recentSongs.length > 10) {
        this.recentSongs.pop()
      }
    },
    async fetchCurrentSong() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:8000/songtracker/update-song/')
        this.currentSong = response.data.song
        this.loading = false
      } catch (error) {
        this.error = 'Fehler beim Abrufen des aktuellen Songs'
        this.loading = false
      }
    },
    async fetchRecentSongs() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:8000/songtracker/recent-songs/')
        this.recentSongs = response.data.songs
        this.loading = false
      } catch (error) {
        this.error = 'Fehler beim Abrufen der letzten Songs'
        this.loading = false
      }
    },
    async fetchSongStats(title, artist, days = 7) {
      this.loading = true
      try {
        const response = await axios.get(`http://localhost:8000/songtracker/song-stats/?title=${encodeURIComponent(title)}&artist=${encodeURIComponent(artist)}&days=${days}`)
        this.songStats = response.data
        this.loading = false
      } catch (error) {
        this.error = 'Fehler beim Abrufen der Song-Statistiken'
        this.loading = false
      }
    },
    async fetchSongWeeklyStats(weeks = 12) {
      let title = this.songWeeklyStatsTitle
      let artist = this.songWeeklyStatsArtist
      this.loading = true
      try {
        const response = await axios.get(`${API_BASE_URL}/songtracker/song-weekly-stats/`, {
          params: {
            title: title ? encodeURIComponent(title) : undefined,
            artist: artist ? encodeURIComponent(artist) : undefined,
            weeks: weeks
          }
        })
        if (response.data.status === "success") {
          this.songWeeklyStats = response.data.weekly_stats
        } else {
          this.songWeeklyStats = null
        }
        this.error = null
        this.loading = false
      } catch (error) {
        this.error = 'Fehler beim Abrufen der wöchentlichen Song-Statistiken'
        this.songWeeklyStats = null
        this.loading = false
        console.error('Fehler beim Abrufen der wöchentlichen Song-Statistiken:', error)
      }
    }
  }
})