<template>
  <div class="card mx-auto mt-3" style="max-width: 800px;" v-if="listaNotas && listaNotas.length > 0">
      <div class="card-header">
         Notas
      </div>
      <div class="card-body">
        <table class="table table-hover">
          <thead>
          <tr>
            <th scope="col">Fecha</th>
            <th scope="col">Nota</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="nota in listaNotas" :key="nota.id">
            <td>{{ nota.creation_date }}</td>
            <td>{{ nota.note }}</td>
          </tr>
        </tbody>
        </table>
      </div>
  </div>

  <div class="card mx-auto mt-3" style="max-width: 800px;" v-else-if="listaNotas && listaNotas.length === 0">
      <div class="card-header">
         Notas
      </div>
      <div class="card-body">
        <p>No hay notas.</p>
      </div>
  </div>
  <br>
  <Form @submit="addNote" ref="myForm">
  <div class="input-group mx-auto mb-3" style="max-width: 800px;">
      <Field
        name="text_note"
        type="text" 
        class="form-control me-2" 
        placeholder="Escriba aqui su nota..."  
        v-model="form.text_note"
        :rules="isRequired" 
      />
      <div class="input-group-append">
        <button class="btn btn-success me-1" type="submit"><i class="bi bi-send"></i> Enviar</button>
        <router-link to="/request" class="btn btn-secondary"><i class="bi bi-x-lg"></i> Cancelar</router-link>
      </div>
  </div>
  <div  class="input-group mx-auto mb-3" style="max-width: 800px;">
    <ErrorMessage class="text-danger" name="text_note"/>
  </div>
  
</Form>
  
</template>

<script>
import axios from 'axios';
import { Form, Field, ErrorMessage } from 'vee-validate';

export default {
  components: {
    Form,
    Field,
    ErrorMessage
  },
  name: "ServiceNote",
  data() {
    return {
      listaNotas: null,
      showTable: false, // Variable para controlar la visibilidad de la tabla
      errorMessage: '',
      service_request_id: null,
      form: {
        "text_note": "",
      }
    }
  },

 
  methods: { 
    isRequired(value) {
      if (value && value.trim()) {
        return true;
      }
      return 'Por favor, completa este campo.';
    },
    async loadServiceNotas() {
        this.miToken = localStorage.getItem('token');
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.miToken}`,
            },
        };
        this.service_request_id = this.$route.params.id;

        try {
            const response = await axios.get(
                `https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/me/requests/${this.service_request_id}/notes/`,
                config
            );
            console.log(response.data)
            console.log(response.data.notes[0])
            this.listaNotas = response.data.notes;
        } catch (error) {
            console.error('Error al cargar las notas del servicio:', error);
            // Manejar el error según sea necesario
        }
    },
    addNote(){
      console.log("Agregando nota...")
      console.log(this.miToken)
      //Configuración del encabezado
      const config = {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.miToken}`,
        },
      };
      this.service_request_id = this.$route.params.id;

      //Configuracion credenciales
      axios.defaults.withCredentials = false;

      axios.post(`https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/me/requests/${this.service_request_id}/notes/`, this.form, config)
        .then(response => {
          if (response.status === 201) {
            console.log('La nota ha sido agregada correctamente');
            console.log(response.data);
            // Después de agregar la nota, recargamos la lista de notas
            this.loadServiceNotas();
            // Reseteamos el valor del Field
            this.$refs.myForm.setFieldValue('text_note', '');

          }
        })
        .catch(error => {
          console.error('Error al realizar la solicitud:', error);
        });

    }


  },
  
  mounted() {
    const isAuthenticated = localStorage.getItem('token') !== null;

    if (isAuthenticated) {
      // Recupera el id del servicio desde los parámetros de la ruta
      this.miToken = localStorage.getItem('token');
    } else {
      // Redirige al formulario de inicio de sesión si no está autenticado
      this.$router.push({ name: 'Login' });
    }
    this.loadServiceNotas();
    
  },

};
</script>
