<template>
  <header>
    <nav class="navbar navbar-dark bg-dark fixed-top">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/"><img src="@/assets/cidepintlogo.png" alt="Logo" width="25" /> CIDEPINT</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasDarkNavbar"
          aria-controls="offcanvasDarkNavbar" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="offcanvas offcanvas-end text-bg-dark" tabindex="-1" id="offcanvasDarkNavbar"
          aria-labelledby="offcanvasDarkNavbarLabel">
          <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasDarkNavbarLabel">Menú</h5>
            <button ref="closeButton" type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"
              aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
              <li class="nav-item">
                <router-link class="nav-link" aria-current="page" to="/login" @click.prevent="toggleDropdown">Iniciar Sesión</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/register" @click.prevent="toggleDropdown">Registrarse</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/service" @click.prevent="toggleDropdown">Buscar servicio</router-link>
              </li>
              <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Gráficos
                  </a>
                  <ul class="dropdown-menu dropdown-menu-dark">
                    <li><router-link class="dropdown-item" to="/chart/bar" @click.prevent="toggleDropdown">Servicios más solicitados</router-link></li>
                    <li><router-link class="dropdown-item" to="/chart/line" @click.prevent="toggleDropdown">TOP 10 Instituciones más eficientes</router-link></li>
                    <li><router-link class="dropdown-item" to="/chart/doughnut" @click.prevent="toggleDropdown">Cantidad de solicitudes por estado</router-link></li>
                    <!-- <li>
                      <hr class="dropdown-divider">
                    </li>
                    <li><a class="dropdown-item" href="#">Something else here</a></li> -->
                  </ul>
                </li>
            </ul>
            <!-- <form class="d-flex mt-3" role="search">
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-success" type="submit">Search</button>
              </form> -->
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>
  
<script>
export default {
  name: "Navbar",
  methods: {
    toggleDropdown() {
      const closeButton = this.$refs.closeButton;
      if (closeButton) {
        closeButton.click();
      }
    },
  },
};
</script>
  
  