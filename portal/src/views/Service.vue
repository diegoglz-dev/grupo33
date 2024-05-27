<template>
  <div class="card mx-auto" style="max-width: 800px;">
      <div class="card-header">
        <i class="bi bi-search"></i> Buscar servicios
      </div>
      <div class="card-body">
        <div class="d-flex mt-3" role="search">
          <input class="form-control me-2" type="search" placeholder="Buscar por nombre, descripcion, palabras clave" aria-label="Search" v-model="searchText">
          <select class="form-select me-2" aria-label="Default select example" v-model="selectedServiceType">
            <option value="">Todos</option>
            <option v-for="serviceType in serviceTypes" :key="serviceType" :value="serviceType">
              {{ serviceType }}
            </option>
          </select>
          <button class="btn btn-success" @click="search">Buscar</button>
        </div>
      </div>
  </div>

  <div class="card mx-auto mt-3" style="max-width: 800px;" v-if="listaServicios && listaServicios.length > 0">
      <div class="card-header">
        <i class="bi bi-list-stars"></i> Listado de servicios
      </div>
      <div class="card-body">
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Nombre</th>
            <th scope="col">Descripción</th>
            <th scope="col">Palabras claves</th>
            <th scope="col">Tipo de servicio</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="servicio in listaServicios" :key="servicio.id" v-on:click="detalle(servicio.id)">
            <th scope="row">{{ servicio.name }}</th>
            <td>{{ servicio.description }}</td>
            <td>{{ servicio.keywords }}</td>
            <td>{{ servicio.type_of_service }}</td>
          </tr>
        </tbody>
        </table>
        <!-- Mostrar controles de paginación -->
        <nav aria-label="Page navigation" class="d-flex justify-content-end">
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

  <div class="card mx-auto mt-3" style="max-width: 800px;" v-else-if="listaServicios && listaServicios.length === 0">
      <div class="card-header">
        <i class="bi bi-list-stars"></i> Listado de servicios
      </div>
      <div class="card-body">
        <p>No se encontraron resultados.</p>
      </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Service",
  data() {
    return {
      listaServicios: null,
      searchText: '',
      selectedServiceType: null,
      serviceTypes: [],
      showTable: false, // Variable para controlar la visibilidad de la tabla
      errorMessage: '',
      pagination: {},
    }
  },

  mounted() {
    this.loadServiceTypes();
    this.selectedServiceType = '';
  },

  methods: {
    detalle(id){
      console.log(id)
      this.$router.push('/service/detail/' + id);
    },

    loadServiceTypes() {
       //Configuracion credenciales
      axios.defaults.withCredentials = false;
      axios.get("https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/services-types/")
        .then((response) => {
          this.serviceTypes = response.data.data;
        })
        .catch((error) => {
          console.error("Error al cargar los tipos de servicios", error);
        });
    },

    search() {
      const apiUrl = "https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/services/search";
      const params = {
        q: this.searchText,
        type: this.selectedServiceType,
        page: this.pagination.page, 
      };

      axios.get(apiUrl, { params })
        .then((response) => {
          console.log(response)
          this.listaServicios = response.data.data[0];
          this.pagination = response.data;
          // Mostrar la tabla después de obtener resultados
          this.showTable = true;
        })
        .catch((error) => {
          console.error("Error al realizar la búsqueda", error);

          // Manejar el código de respuesta 400
          if (error.response && error.response.status === 400) {
            this.showTable = false;
            this.errorMessage = 'Ingrese el nombre del servicio.';
          } else {
            this.errorMessage = 'Error al realizar la búsqueda.';
          }
        });
    },
    changePage(page) {
      // Cambiar la página y realizar una nueva búsqueda
      this.pagination.page = page;
      this.search();
    },

  },
};
</script>

<style>
tbody tr:hover {
  cursor: pointer;
}
</style>