<template>
    <h1 class="mb-3">Mis solicitudes</h1>
    <div class="container">
      <div class="row align-items-start" v-if="listaServicios && listaServicios.length > 0">
        <div class="col-4" v-for="servicio in listaServicios" :key="servicio.id">
        <div class="card mx-auto">
            <div class="card-header">
              <i class="bi bi-journal-text"></i> {{ servicio.title }}
            </div>
            <div class="card-body">
              <p><b>Descripción: </b><br>{{ servicio.description }}</p>
              <p><b>Estado: </b><br>{{ servicio.status }}</p>
              <p><b>Fecha de creación: </b><br>{{ servicio.creation_date }}</p>
              <p><b>Fecha de cierre</b><br>
                <span v-if="servicio.close_date">{{ servicio.close_date }}</span>
                <span v-else>Sin fecha de cierre</span>
              </p>

                <button class="btn btn-primary" @click="notes(servicio.id)"><i class="bi bi-eye"></i> Ver</button>
            </div>
        </div>
      </div>
      <!-- Mostrar controles de paginación -->
      <div class="d-flex justify-content-between align-items-center">
        <router-link to="/service" class="btn btn-secondary"><i class="bi bi-backspace"></i> Volver</router-link>
        
        <nav aria-label="Page navigation" class="d-flex justify-content-end align-items-end">
          <ul class="pagination">
            <li class="page-item" :class="{ disabled: pagination.page === 1 }">
              <button class="page-link" @click="changePage(pagination.page - 1)" :disabled="pagination.page === 1">Anterior</button>
            </li>
            <li class="page-item" v-for="pageNumber in Math.ceil(pagination.total / pagination.per_page)" :key="pageNumber" :class="{ active: pageNumber === pagination.page }">
              <button class="page-link" @click="changePage(pageNumber)">{{ pageNumber }}</button>
            </li>
            <li class="page-item" :class="{ disabled: pagination.page === Math.ceil(pagination.total / pagination.per_page) }">
              <button class="page-link" @click="changePage(pagination.page + 1)" :disabled="pagination.page === pagination.total">Siguiente</button>
            </li>
          </ul>
        </nav>
      </div>

    </div>

    <div v-else-if="listaServicios && listaServicios.length === 0">
      <div class="alert alert-info" role="alert">
        No posee solicitudes asociadas.
      </div>
      <router-link to="/service" class="btn btn-secondary mt-4"><i class="bi bi-backspace"></i> Volver</router-link>
    </div>

  </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: "ServiceRequest",
    data() {
      return {
        listaServicios: null,
        errorMessage: '',
        miToken: "",
        pagination: {},
      };
    },
  
    methods: {
      loadService() {
        this.miToken = localStorage.getItem('token');
        const config = {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.miToken}`,
          },
        };
  
        axios.get('https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/me/requests/',  { params: { page: this.pagination.page }, headers: config.headers})
          .then((response) => {
            console.log(response.data.data[0]);
            this.listaServicios = response.data.data[0];
            this.pagination = response.data;
            // Establecer showTable en true después de cargar los servicios
            // para mostrar la tabla.
            this.showTable = true;
          })
          .catch((error) => {
            console.error("Error al cargar las solicitudes", error);
          });
      },
      changePage(page) {
        // Cambiar la página y realizar una nueva búsqueda
        this.pagination.page = page;
        this.loadService();
      },
      notes(id) {
        console.log(id);
        this.$router.push({ name: 'ServiceNote', params: { id: id } });
      },
    },
  
    mounted() {
      const isAuthenticated = localStorage.getItem('token') !== null;
  
      if (isAuthenticated) {
        this.miToken = localStorage.getItem('token');
      } else {
        this.$router.push({ name: 'Login' });
      }
  
      this.loadService();
    },
  };
  </script>
  