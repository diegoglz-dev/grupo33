<template>
  <h1 class="mb-3">Servicios más solicitados</h1>
  <Bar :data="data" :options="options" />
</template>

<script lang="ts">
import axios from 'axios';
import {
BarElement,
CategoryScale,
Chart as ChartJS,
Legend,
LinearScale,
Title,
Tooltip,
} from 'chart.js';
import { Bar } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default {
  name: 'App',
  components: {
    Bar,
  },
  data() {
    return {
      data: {
        labels: [],
        datasets: [
          {
            label: 'Total Requests',
            backgroundColor: '#FF6384',
            data: [],
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            stepSize: 1,
            precision: 0,
          },
        },
      },
    };
  },
  mounted() {
    // Realizar la solicitud HTTP al servidor
    axios.get('https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/services/most_requested')
      .then(response => {
        // Actualizar los datos del gráfico con la respuesta del servidor
        const newData = {
          labels: response.data.map(item => item.name),
          datasets: [
            {
              label: 'Total de Solicitudes',
              backgroundColor: '#FF6384',
              data: response.data.map(item => item.total_requests),
            },
          ],
        };
        this.data = newData;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  },
};
</script>
