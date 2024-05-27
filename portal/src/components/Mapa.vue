<template>
  <div id="mapContainer"></div>
</template>

<script>
import { defineComponent, onMounted, onBeforeUnmount, watch } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import 'leaflet/dist/images/marker-shadow.png';

export default defineComponent({
  props: {
    markers: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  setup(props, { refs }) {
    let map = null;
    let markersLayer = null;
    let initialized = false;

    const setMarkers = () => {
      console.log('Calling setMarkers...');
      if (markersLayer) {
        markersLayer.clearLayers();

        if (props.markers && props.markers.length) {
          props.markers.forEach((markerData) => {
            const { localizacion, name, contacto, web, dias_horarios } = markerData;

            try {
              const [lat, lon] = localizacion.split(",").map(Number);
              console.log("Adding marker:", name, localizacion);

              // Personaliza el contenido del popup con la información adicional
              const popupContent = `
            <strong>${name}</strong><br><br>
            <em>Contacto:</em> ${contacto}<br>
            <em>Web:</em> ${web}<br>
            <em>Dias y Horarios:</em> ${dias_horarios}
          `;

              const newMarker = L.marker([lat, lon], {
                icon: L.icon({ iconUrl: markerIcon, iconSize: [25, 25], iconAnchor: [15, 30] }),
              }).bindPopup(popupContent);

              markersLayer.addLayer(newMarker);
            } catch (error) {
              console.error("Error adding marker:", error);
              console.log("Failed to add marker for:", name, localizacion);
            }
          });

          // Calcular la posición del centro del mapa y el nivel de zoom
          const [firstLat, firstLon] = props.markers[0].localizacion.split(",").map(Number);
          const newZoom = 15;  // Ajusta el nivel de zoom según tus preferencias

          map.setView([firstLat, firstLon], newZoom);
        }
      } else {
        console.error('Markers layer not initialized.');
      }
    };

    onMounted(() => {
      console.log('Component mounted');
      const mapContainer = document.getElementById('mapContainer');

      if (!initialized) {
        markersLayer = L.layerGroup();
        map = L.map('mapContainer').setView([-34.6, -58.4], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
          maxZoom: 18
        }).addTo(map);

        // Agregar la capa de marcadores al mapa
        if (map) {
          markersLayer.addTo(map);
        } else {
          console.error('Map not initialized.');
        }

        // Llamar a la función para establecer los marcadores
        setMarkers();

        // Marcar como inicializado
        initialized = true;
      }
    });

    onBeforeUnmount(() => {
      console.log('Component unmounted');
      if (map) {
        map.remove();
      }
    });

    watch(() => props.markers, (newMarkers) => {
      // Actualizar marcadores solo si hay cambios
      if (newMarkers.length !== props.markers.length) {
        setMarkers();
      }
    });

    // Exponer setMarkers en el objeto setup
    return {
      setMarkers,
    };
  },
});
</script>

<style scoped>
#mapContainer {
  height: 300px;
  width: 300px;
}
</style>
