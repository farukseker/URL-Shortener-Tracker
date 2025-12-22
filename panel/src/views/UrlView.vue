<template>
    x
    {{ url_data }}
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';

const { url_code } = defineProps(['url_code'])

const url_data = ref(null) 

const load_url_data = async () => {
    var r = await axios.get(`/admin/url`, {params: {code: url_code}})
    url_data.value = r.data
}

onMounted(load_url_data)
</script>