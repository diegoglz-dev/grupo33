<template>
    <div>
      <h1 class="mb-4">Solicitud de servicio</h1>
      <div class="card-body">
        <div class="row">
          <div class="col-sm-6">
            <p><strong>Nombre:</strong> {{ service.name }}</p>
          </div>
          <div class="col-sm-6">
            <p><strong>Tipo de servicio:</strong> {{ service.type_of_service }}</p>
          </div>
          <div class="col-sm-6">
            <p><strong>Palabras clave:</strong> {{ service.keywords }}</p>
          </div>
          <div class="col-sm-6">
            <p><strong>Descripción:</strong> {{ service.description }}</p>
          </div>
        </div>
        <!-- Mostrar el botón de solicitud solo si el servicio está habilitado -->
        <button v-if="service.enabled" type="button" class="btn btn-dark margen" @click="solicitar">
          <i class="bi bi-send-plus"></i> Solicitar
        </button>
      </div>
  
      <div>
        <h2 class="mt-4">¿Como llegar?</h2>
        <br>
        <MapComponent ref="mapComponent" :markers="locations" />
      </div>
    </div>
    <router-link to="/service" class="btn btn-secondary mt-4"><i class="bi bi-backspace"></i> Volver</router-link>
  </template>
  
<script>
import MapComponent from "@/components/Mapa.vue";
import axios from 'axios';
  
  export default {
    name: "ServiceDetail",
    components: {
      MapComponent,
    },
    data() {
      return {
        service_id: null,
        service: {},
        locations: [],
      };
    },
    methods: {
      solicitar() {
          const isAuthenticated = localStorage.getItem('token') !== null;

          if (isAuthenticated) {
            // Redirige a la vista del formulario de solicitud con el id del servicio
            this.$router.push({ name: 'FormServiceRequest', params: { id: this.service_id } });
          } else {
            // Redirige al formulario de inicio de sesión si no está autenticado
            this.$router.push({ name: 'Login' });
          }
      },
      async fetchLocations() {
        try {
          this.service_id = this.$route.params.id;
          // Obtener ubicaciones para el mapa
          const response = await axios.get(`https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/institutions/find_inst_by_service/${this.service_id}`
          , { withCredentials: true });
          this.locations = response.data.data;
  
          // Actualizar marcadores en el mapa
          this.$nextTick(() => {
            if (this.$refs.mapComponent && this.$refs.mapComponent.setMarkers) {
              this.$refs.mapComponent.setMarkers(this.locations);
            } else {
              console.error("Ref or setMarkers method not defined.");
            }
          });
        } catch (error) {
          console.error("Error fetching locations:", error);
        }
      },
    },
    mounted() {
      this.service_id = this.$route.params.id;
      // Obtener detalles del servicio
      axios.get(`https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/services/${this.service_id}`, { withCredentials: true })
        .then(response => {
          this.service = response.data;
        })
        .catch(error => {
          console.error('Error al obtener los datos del servicio:', error);
        });
  
      this.fetchLocations();
    },
  };
  </script>
  