<template>
  <div class="p-5 mb-4 bg-body-tertiary rounded-3">
    <div class="container-fluid py-5">
      <div v-if="!isLogin">
        <h1 class="display-5 fw-bold">Bienvenidos a CIDEPINT</h1>
      </div>
      <div v-if="isLogin">
        <h1 class="display-5 fw-bold">Bienvenidx {{ nombre }} {{ apellido }}</h1>
      </div>
      
      <p class="col-md-8 fs-4">Descubrí todas las funciones de nuestro sistema al completar tu registro y accede a información de interés, incluyendo datos sobre el Laboratorio, detalles institucionales y los servicios disponibles.</p>
      <div v-if="isLogin">
        <button class="btn btn-primary btn-lg" type="button" @click="logout">Cerrar sesión</button>
      </div>
    </div>
  </div>

  <div class="row align-items-md-stretch">
    <div class="col-md-4">
      <div class="h-100 p-5 text-bg-dark rounded-3">
        <h2>Búsquedas de servicios.</h2>
        <p>Consulta la lista completa de servicios ofrecidos por cada institución.</p>
        <router-link to="/service" class="btn btn-outline-light" type="button">Buscar</router-link>
      </div>
    </div>
    <div class="col-md-4">
      <div class="h-100 p-5 bg-body-tertiary border rounded-3">
        <h2>Solicitudes</h2>
        <p>Esta funcionalidad te permitirá estar al tanto de los progresos de tus pedidos y realizar aportes importantes mediante comentarios o aclaraciones adicionales</p>
        <button type="button"  class="btn btn-outline-secondary" @click="consultar">Consultar</button>
      </div>
    </div>
    <div class="col-md-4">
      <div class="h-100 p-5 text-bg-dark rounded-3">
        <h2>¿Sos dueño de una institución?</h2>
        <p>Podrás visualizar gráficamente información estadística relevante, como por ejemplo, un ranking de los servicios más solicitados.</p>
        <router-link to="/chart/bar" class="btn btn-outline-light" type="button">Visualizar</router-link>
      </div>
    </div>
  </div>

  <div class="row align-items-md-stretch">
    <div class="col-md-3"></div>
    <div class="col-md-6">
      <div class="card mb-5 mt-5">
      <img src="@/assets/conicet.jpg" class="card-img-top" alt="...">
      <div class="card-body">
          <h5 class="card-title">¿Quienes somos?</h5>
          <p class="card-text">El Centro de Investigación y Desarrollo en Pinturas (CIDEPINT) es un laboratorio de investigación y desarrollo de pinturas y recubrimientos, que brinda servicios de análisis y ensayos a la industria y a la comunidad científica.</p>
        </div>
      </div>
    </div>
    <div class="col-md-3"></div>
  </div>
</template>

<script>
import Footer from "@/components/layouts/Footer.vue";
export default {
  name: "Home",
  data() {
    return {
      nombre: "",
      apellido: "",
      email: "",
      isLogin: false,
    };
  },
  components: {
    Footer,
  },
  mounted() {
    // Verificar si el usuario ya inició sesión
    if (localStorage.getItem("token")) {
      this.isLogin = true;
      this.nombre = localStorage.getItem("user_first_name");
      this.apellido = localStorage.getItem("user_last_name");
      this.email = localStorage.getItem("user_email");
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.isLogin = false;
      this.$router.push("/login");
    },
    consultar() {
          const isAuthenticated = localStorage.getItem('token') !== null;

          if (isAuthenticated) {
            // Redirige a la vista del formulario de solicitud con el id del servicio
            this.$router.push({ name: 'ServiceRequest' });
          } else {
            // Redirige al formulario de inicio de sesión si no está autenticado
            this.$router.push({ name: 'Login' });
          }
      },
  },
};
</script>
