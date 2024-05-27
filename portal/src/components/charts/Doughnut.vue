<template>
  <h1 class="mb-3">Cantidad de solicitudes por estado</h1>
  <div class="doughnut-container">
    <Doughnut :data="chartData" :key="chartKey" />
  </div>
</template>
  
<script lang="ts">
import axios from 'axios';
import { ArcElement, Chart as ChartJS, Legend, Tooltip } from 'chart.js';
import { Doughnut } from 'vue-chartjs';

ChartJS.register(ArcElement, Tooltip, Legend)

export default {
  name: 'DoughnutChart',
  components: {
    Doughnut
  },
  data() {
    return {
      chartData: {
        labels: [],
        datasets: [
          {
            data: [],
            backgroundColor: [],
            hoverBackgroundColor: []
          }
        ]
      },
      chartKey: 0  // Agrega una clave única para forzar la actualización del componente
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get('https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/me/requests/solicitudes_por_estado')
        .then(response => {
          const data = response.data;

          this.chartData.labels = Object.keys(data);
          this.chartData.datasets[0].data = Object.values(data);
          this.chartData.datasets[0].backgroundColor = ['#FF6384', '#36A2EB', '#FFCE56'];
          this.chartData.datasets[0].hoverBackgroundColor = ['#FF6384', '#36A2EB', '#FFCE56'];

          // Incrementa la clave única para forzar la actualización del componente
          this.chartKey += 1;
        })
        .catch(error => {
          console.error('Error al obtener datos de la API:', error);
        });
    }
  }
};
</script>

<style scoped>
.doughnut-container {
  width: 700px;
  height: 700px;
}
</style>
  