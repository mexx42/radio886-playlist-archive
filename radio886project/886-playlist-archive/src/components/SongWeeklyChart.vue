<!-- src/components/SongWeeklyChart.vue -->

<template>
    <div>
      <h3>Wöchentliche Wiedergaben</h3>
      <div v-if="1">
        <canvas ref="chart"></canvas>
      </div>
      <div v-else>
        Keine Daten verfügbar
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useSongStore } from '../stores/songStore'
  import Chart from 'chart.js/auto'
  
  const store = useSongStore()
  const chart = ref(null)
  const chartData = ref(null)
  
  const createChart = () => {
    if (chart.value) {
      chart.value.destroy()
    }
  
    const ctx = document.getElementById('weeklyChart').getContext('2d')
    chart.value = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: chartData.value.labels,
        datasets: chartData.value.datasets
      },
      options: {
        responsive: true,
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
  
  watch(() => store.songWeeklyStats, (newStats) => {
    if (newStats) {
      chartData.value = formatChartData(newStats);
      createChart();
    }
  })
  
  onMounted(() => {
    if (store.songWeeklyStats) {
      chartData.value = formatChartData(store.songWeeklyStats);
      createChart();
    }
  })
  </script>