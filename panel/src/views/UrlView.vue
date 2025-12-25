<template>
<section class="w-full flex justify-center h-screen absolute top-0 left-0 py-20 overflow-auto">
    <article class="m-auto">
        <UrlForm />
    </article>
</section>

</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useUrlStore } from '@/stores/url_form_store';
import { storeToRefs } from "pinia";
import UrlForm from '@/components/form/UrlForm.vue'

const { url_code } = defineProps(['url_code'])
const url_store = useUrlStore()

const { id, url, url_type, slug, categories } = storeToRefs(url_store)

const load_url_data = async () => {
    url_store.load_url_data(await url_store.get_url(url_code))
}

onMounted(load_url_data)
</script>