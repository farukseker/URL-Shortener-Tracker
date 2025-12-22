<template>
    <iframe 
        :src="url"
        title="Video player"
        frameborder="0"
        width="100%"
        height="350"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        referrerpolicy="strict-origin-when-cross-origin" 
        allowfullscreen
    ></iframe>
</template>

<script setup>
const { url } = defineProps(['url'])
</script>