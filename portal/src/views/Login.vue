<template>
    <div class="card mx-auto" style="max-width: 400px;">
        <div class="card-header">
            Iniciar sesión
        </div>
        <div class="card-body">
            <form @submit.prevent="submitForm">
                <div class="mb-3">
                    <label for="exampleInputEmail1" class="form-label">Usuario o correo</label>
                    <input type="text" class="form-control" id="exampleInputEmail1" v-model="email" required autofocus>
                </div>
                <div class="mb-3">
                    <label for="exampleInputPassword1" class="form-label">Contraseña</label>
                    <input type="password" class="form-control" id="exampleInputPassword1" v-model="password" required>
                </div>
                <button type="submit" class="btn btn-primary">Ingresar</button>
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
    name: "Login",
    data() {
        return {
            email: '',
            password: '',
            errorMessages: [],
        };
    },
    mounted() {
        // Verificar si el usuario ya inició sesión
        if (localStorage.getItem('token')) {
            this.$router.push('/');
        }
    },
    methods: {
        submitForm() {
            this.errorMessages = [];
            // Realizar la solicitud POST a la URL
            // axios.post('http://127.0.0.1:5000/api/auth/login', {
            axios.post('https://admin-grupo33.proyecto2023.linti.unlp.edu.ar/api/auth/login', {
                email: this.email,
                password: this.password,
            })
            .then(response => {
                // Manejar la respuesta exitosa, por ejemplo, almacenar el token o redirigir a otra página
                console.log(response.data);
                localStorage.setItem('token', response.data.token);
                localStorage.setItem('user_first_name', response.data.user_first_name);
                localStorage.setItem('user_last_name', response.data.user_last_name);
                localStorage.setItem('user_email', response.data.user_email);
                this.$router.push('/'); // Redirigir a la página de inicio
            })
            .catch(error => {
                // Manejar errores, por ejemplo, mostrar un mensaje de error al usuario
                console.error('Error al iniciar sesión:', error);

                // Manejar el error
                if (error.response && error.response.data && error.response.data.error) {
                    // Mostrar errores de validación
                    this.errorMessages.push(error.response.data.error);
                } else {
                    // Manejar otros errores
                    console.error(error);
                }
            });
        },
    },
}

</script>

<style>

</style>