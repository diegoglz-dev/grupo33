<template>
  <div class="card mx-auto" style="max-width: 500px;">
      <div class="card-header">
          Registrarse
      </div>
      <div class="card-body">
          <form @submit.prevent="registro">
              <div class="mb-3">
                  <label for="exampleInputName" class="form-label">Nombre</label>
                  <input type="text" class="form-control" id="exampleInputName" v-model="first_name" required autofocus>
              </div>
              <div class="mb-3">
                  <label for="exampleInputLastName" class="form-label">Apellido</label>
                  <input type="text" class="form-control" id="exampleInputLastName" v-model="last_name" required>
              </div>
              <div class="mb-3">
                  <label for="exampleInputUsername" class="form-label">Nombre de Usuario</label>
                  <input type="text" class="form-control" id="exampleInputUsername" v-model="username" required>
              </div>
              <div class="mb-3">
                  <label for="exampleInputEmail1" class="form-label">Email</label>
                  <input type="email" class="form-control" id="exampleInputEmail1" v-model="email" required>
              </div>
              <div class="mb-3">
                  <label for="exampleInputPassword1" class="form-label">Contraseña</label>
                  <input type="password" class="form-control" id="exampleInputPassword1" v-model="password" required>
              </div>
              <div class="mb-3">
                  <label for="exampleInputPassword2" class="form-label">Confirmar contraseña</label>
                  <input type="password" class="form-control" id="exampleInputPassword2" v-model="password_confirmation" required>
              </div>
              <button type="submit" class="btn btn-primary">Registrarse</button>
              <div v-if="errorMessages.length > 0" style="color: red; margin-top: 10px;">
                  <ul>
                      <li v-for="error in errorMessages" :key="error">{{ error }}</li>
                  </ul>
              </div>
          </form>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
axios.defaults.headers.common['crossorigin'] = 'true';
export default {
    name: "Register",
    data() {
    return {
      first_name: '',
      last_name: '',
      username: '',
      email: '',
      password: '',
      password_confirmation: '',
      errorMessages: []
    };
  },
  mounted() {
      // Verificar si el usuario ya inició sesión
      if (localStorage.getItem('token')) {
          this.$router.push('/');
      }
  },
  methods: {
    registro() {
      this.errorMessages = [];
      const formData = {
        first_name: this.first_name,
        last_name: this.last_name,
        username: this.username,
        email: this.email,
        password: this.password,
        password_confirmation: this.password_confirmation,
        errorMessages: []
      };

        // axios.post('http://127.0.0.1:5000/api/auth/register', formData)
        axios.post('https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/auth/register', formData)
        .then(response => {
            // Manejar la respuesta exitosa
            console.log(response.data);
            localStorage.setItem('token', response.data.token);
            localStorage.setItem('user_first_name', response.data.user_first_name);
            localStorage.setItem('user_last_name', response.data.user_last_name);
            localStorage.setItem('user_email', response.data.user_email);
            this.$router.push('/'); // Redirigir a la página de inicio
        })
        .catch(error => {
          if (error.response && error.response.data && error.response.data.error) {
            // Mostrar errores de validación
            this.errorMessages.push(error.response.data.error);
          } else {
            // Manejar otros errores
            console.error(error);
          }
        });
    }
  }
}
</script>