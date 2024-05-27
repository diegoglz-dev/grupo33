<template>
  <div class="card mx-auto" style="max-width: 800px;">
      <div class="card-header">
          Solicitud de servicio
      </div> 
      <div class="card-body">
        <Form @submit="save">
          <div class="mb-3">
              <label for="title" class="form-label">Título</label>
              <Field 
                  name="title" 
                  type="text" 
                  class="form-control" 
                  id="title" 
                  v-model="form.title" 
                  placeholder="Ingrese título" 
                  :rules="isRequired" 
              />
              <ErrorMessage class="text-danger" name="title"/>
          </div>
          <div class="mb-3">
              <label for="description" class="form-label">Descripción</label>
              <Field 
                  as="textarea" 
                  name="description" 
                  type="text" 
                  class="form-control" 
                  id="description" 
                  v-model="form.description" 
                  placeholder="Ingrese descripción" 
                  :rules="isRequired" 
              />
              <ErrorMessage class="text-danger" name="description"/>
          </div>
          <button type="submit" class="btn btn-primary me-2"><i class="bi bi-send"></i> Enviar solicitud</button>
          <router-link to="/service" class="btn btn-secondary"><i class="bi bi-x-lg"></i> Cancelar</router-link>
        </Form>
      </div>
  </div>
</template>

<script>
import axios from "axios";
import { Form, Field, ErrorMessage } from 'vee-validate';

export default {
  components: {
    Form,
    Field,
    ErrorMessage
  },
name: "FormServiceRequest",
data() {
  return {
    submited: false,
    form: {
      "service_id": "",
      "title": "",
      "description": "",
    },
    miToken: " ",

  };
},
methods: {
  isRequired(value) {
      if (value && value.trim()) {
        return true;
      }
      return 'Por favor, completa este campo.';
    },
  save() {
    console.log("apunto de guardar algo...")
    console.log(this.miToken)
    //Configuración del encabezado
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.miToken}`,
      },
    };

    //Configuracion credenciales
    axios.defaults.withCredentials = false;

    axios.post('https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/me/requests/', this.form, config)
      .then(response => {
        if (response.status == 201) {
          console.log('Solicitud exitosa');
          console.log(response.data);
          this.$router.push({ name: 'ServiceRequest'});
         
        }
      })
      .catch(error => {
        console.error('Error al realizar la solicitud:', error);
      });
  },
},


mounted() {
  const isAuthenticated = localStorage.getItem('token') !== null;

  if (isAuthenticated) {
    // Recupera el id del servicio desde los parámetros de la ruta
    this.miToken = localStorage.getItem('token');
    this.form.service_id = this.$route.params.id;
  } else {
    // Redirige al formulario de inicio de sesión si no está autenticado
    this.$router.push({ name: 'Login' });
  }
}
}
</script>

<style>

</style>

