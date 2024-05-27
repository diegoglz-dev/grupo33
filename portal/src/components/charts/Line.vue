<template>
  <h1 class="mb-3">TOP 10 Instituciones más eficientes</h1>
  <Line :data="data" />
</template>

<script lang="ts">
import axios from 'axios';
import {
CategoryScale,
Chart as ChartJS,
Legend,
LineElement,
LinearScale,
PointElement,
Title,
Tooltip,
} from 'chart.js';
import { Line } from 'vue-chartjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: 'App',
  components: {
    Line,
  },
  data() {
    return {
      data: {
        labels: [], // Aquí debes proporcionar las etiquetas adecuadas para tus instituciones
        datasets: [
          {
            label: 'Tiempo de Resolución',
            backgroundColor: 'rgba(179,181,198,0.2)',
            borderColor: 'rgba(179,181,198,1)',
            pointBackgroundColor: 'rgba(179,181,198,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(179,181,198,1)',
            data: [], // Aquí debes proporcionar los tiempos de resolución adecuados
          },
        ],
      },
    };
  },
  mounted() {
    axios.get('https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/institutions/top_institutions_resolution_time')
      .then(response => {
        // Actualizar los datos del gráfico con la respuesta del servidor
        const newData = {
          labels: Object.keys(response.data), // Obtener las instituciones como etiquetas
          datasets: [
            {
              label: 'Tiempo de Resolución en Días',
              backgroundColor: 'rgba(255,0,0,1)', // Color del Label
              borderColor: 'rgba(179,181,198,1)',
              pointBackgroundColor: 'rgba(255,0,0,1)',  // Color del Punto
              pointBorderColor: '#fff',
              pointHoverBackgroundColor: 'rgba(255,0,0,1)',  // Cambia el color del Punto al pasarle el mouse
              pointHoverBorderColor: 'rgba(179,181,198,1)',
              pointRadius: 10,
              data: Object.values(response.data).map(institution => institution.average_resolution_time_days),
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
