<template>
<section class="w-full flex justify-center h-screen absolute top-0 left-0 pt-20 overflow-auto">
    <article class="m-auto">
        <UrlForm @on_save="save" />
    </article>
</section>
</template> 


<script setup>
import UrlForm from '@/components/form/UrlForm.vue'
import { useRouter } from "vue-router";
import { useUrlStore } from '@/stores/url_form_store';
import { onMounted } from 'vue';

const url_store = useUrlStore()

const router = useRouter()

onMounted(url_store.flush_url_data)

const save = async () => {
    var r = await url_store.create_new_url()
    router.push({
        name:'manage-url',
        params: {
            url_code: r.code,
        }
    })
}
</script>