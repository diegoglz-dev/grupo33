<template>
  <footer class="bg-dark text-light py-3 text-center mt-auto">
    <p>&copy; {{ currentYear }} | Desarrollado por {{ developerName }}</p>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      developerName: "Grupo 33",
      currentYear: new Date().getFullYear(),
    };
  },
};
</script>

<style>
footer {
  bottom: 0;
  width: 100%;
}
</style>
