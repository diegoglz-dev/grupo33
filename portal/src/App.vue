<template>
  <div id="app">
    <Navbar />
    <div class="container my-5"><br><br>
      <router-view />
    </div>
    <!-- <Footer /> -->
  </div>
</template>

<script>
import Footer from "@/components/layouts/Footer.vue";
import Navbar from "@/components/layouts/Navbar.vue";

export default {
  name: "App",
  components: {
    Navbar,
    Footer,
  },
};
</script>