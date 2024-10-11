<!-- src/components/SongWeeklyChart.vue -->

<template>
  <div>
    <h2 class="text-xl font-bold mb-2">Wöchentliche Wiedergaben</h2>
    <div>
      <input v-model="store.songWeeklyStatsArtist" placeholder="Künstler eingeben" class="border p-2 mr-2 rounded"/>
      <input v-model="store.songWeeklyStatsTitle" placeholder="Titel eingeben" class="border p-2 mr-2 rounded"/>
      <input v-model="weeks" type="number" placeholder="Wochen" class="border p-2 mr-2 rounded" min="1">
      <button @click="fetchData" class="mt-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
        Aktualisieren
      </button>
   </div>
    <div v-if="chartData" class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
    <div v-else-if="loading">
      Lade Daten...
    </div>
    <div v-else>
      Keine Daten verfügbar
    </div>
    <div v-if="chartError" class="error-message">
      Fehler beim Rendern des Charts: {{ chartError }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { useSongStore } from '../stores/songStore'
import Chart from 'chart.js/auto'

const store = useSongStore()
const chartInstance = ref(null)
const chartCanvas = ref(null)
const chartData = ref(null)
const loading = ref(false)
const chartError = ref(null)
const weeks = ref(12)

const createChart = () => {
  chartError.value = null

  if (chartInstance.value) {
    chartInstance.value.destroy()
  }

  if (chartCanvas.value) {
    try {
      chartInstance.value = new Chart(chartCanvas.value, {
        type: 'bar',
        data: {
          labels: chartData.value.labels,
          datasets: chartData.value.datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
    } catch (error) {
      console.error('Fehler beim Erstellen des Charts:', error)
      chartError.value = error.message
    }
  } else {
    chartError.value = 'Canvas-Element nicht gefunden'
  }
}

const formatChartData = (data) => {
  return {
    labels: data.map(item => {
      const date = new Date(item.week);
      return `${date.getDate()}.${date.getMonth() + 1}.`;
    }),
    datasets: [{
      label: 'Wiedergaben pro Woche',
      data: data.map(item => item.count),
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  };
}

const fetchData = async () => {
  loading.value = true
  await store.fetchSongWeeklyStats(weeks.value)
  loading.value = false
}

watch(() => store.songWeeklyStats, (newStats) => {
  if (newStats) {
    chartData.value = formatChartData(newStats);
    createChart();
  } else {
    chartData.value = null
    if (chartInstance.value) {
      chartInstance.value.destroy()
      chartInstance.value = null
    }
  }
})

onMounted(() => {
  if (store.songWeeklyStats) {
    chartData.value = formatChartData(store.songWeeklyStats);
    createChart();
  }
})

onBeforeUnmount(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy()
  }
})
</script>

<style scoped>
.chart-container {
  height: 400px;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>