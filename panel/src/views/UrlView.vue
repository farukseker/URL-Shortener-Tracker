<template>
<section class="w-full flex justify-center h-screen absolute top-0 left-0 py-20 overflow-auto">
    <article class="m-auto">
        <UrlForm @on_save="on_save" @on_delete="on_delete" />
    </article>
</section>

</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useUrlStore } from '@/stores/url_form_store';
import { storeToRefs } from "pinia";
import UrlForm from '@/components/form/UrlForm.vue'
import { useRouter } from 'vue-router';

const { url_code } = defineProps(['url_code'])
const router = useRouter()
const url_store = useUrlStore()

const { id, url, url_type, slug, categories, pre_slug } = storeToRefs(url_store)

const load_url_data = async () => {
    url_store.load_url_data(await url_store.get_url(url_code))
}

const on_save = async () => {
    await url_store.update_url()
    router.push({
        name: 'manage-url',
        params: {
            url_code: slug.value
        }
    })
} 
const on_delete = async () => {
    await url_store.delete_url(url_code)
    router.push('/')
} 

onMounted(load_url_data)
</script>