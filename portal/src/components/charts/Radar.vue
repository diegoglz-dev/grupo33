<template>
    <Radar :data="data" />
  </template>
  
  <script lang="ts">
  import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
  } from 'chart.js'
  import { Radar } from 'vue-chartjs'
  
  ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend
  )
  
  export default {
    name: 'App',
    components: {
      Radar
    },
    data() {
  return {
    data: {
      labels: ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5"],
      datasets: [{
        label: "Dataset 1",
        backgroundColor: "rgba(179,181,198,0.2)",
        borderColor: "rgba(179,181,198,1)",
        pointBackgroundColor: "rgba(179,181,198,1)",
        pointBorderColor: "#fff",
        pointHoverBackgroundColor: "#fff",
        pointHoverBorderColor: "rgba(179,181,198,1)",
        data: [10, 20, 30, 25, 15]
      }]
    },
  }
    }
        }
  </script>
  