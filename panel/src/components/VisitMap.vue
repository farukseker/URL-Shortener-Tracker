<template>
  <div ref="mapEl" class="h-64 w-full rounded"></div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import L from "leaflet"
import "leaflet/dist/leaflet.css"

const props = defineProps({
  lat: Number,
  lon: Number
})

const mapEl = ref(null)

onMounted(() => {
  const map = L.map(mapEl.value).setView([props.lat, props.lon], 10)

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18
  }).addTo(map)

  L.marker([props.lat, props.lon]).addTo(map)
})
</script>