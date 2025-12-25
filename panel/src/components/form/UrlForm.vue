<template>
    <fieldset class="fieldset bg-base-200 rounded-box w-lg p-4 shadow-xl border border-accent">
        <legend class="fieldset-legend">Url details ({{ id }})</legend>

        <label class="label">Url</label>
        <label class="label input w-full" :class="is_url_allready_use ? 'border border-error':''">
            <Icon class="h-[1em] opacity-50" :icon="faLink" />
            <input v-model="url" type="url" placeholder="Url" />
        </label>
        <p v-if="is_url_allready_use" class="text-error">This url allready using</p>

        <label class="label">Slug (optionel)</label>
        <label class="label input w-full" :class="is_slug_allready_use ? 'border border-error':''">
            <Icon class="h-[1em] opacity-50" :icon="faChain" />
            <input v-model="slug" type="text" placeholder="Slug" />
        </label>
        <p v-if="is_slug_allready_use" class="text-error">This url allready using</p>
        
        <label class="label">Url type</label>
        <label class="label input select w-full">
            <Icon class="h-[1em] opacity-50" :icon="faSlash" />
            <select v-model="url_type">
                <option disabled selected>Url type</option>
                <option value="image">Image</option>
                <option value="video">Video</option>
                <option value="url">Url</option>
            </select>
        </label>
        <label class="label">Url Categories</label>
        <form>
            <input class="btn btn-square" type="reset" value="×" @click="categories = []" />
            <input 
                v-model="categories"
                v-for="(category, index) in categories_list"
                :value="category.id"
                v-bind:key="index"
                class="btn" type="checkbox" name="categories" :aria-label="category.name"/>
        </form>

        <div class="w-full my-2">
            <button class="btn btn-accent float-end" :disabled="!is_correct" @click="save">Save</button>
        </div>

        <hr class="my-4 text-base-100">

        <label>Preview</label>
        <img class="object-cover" v-if="url_type === 'image'" :src="url">
        <VideoPreview v-else-if="url_type === 'video' && url && url.includes('youtube') && url.includes('embed')" :url="url" />
        <a class="font-semibold underline link-accent text-wrap" target="_blank" :href="url">{{ url }}</a>

    </fieldset>
</template>

<script setup>
import VideoPreview from '@/components/VideoPreview.vue'
import { faChain, faLink, faSlash, faTag } from '@fortawesome/free-solid-svg-icons'
import { onMounted, ref, watch } from 'vue'
import axios from 'axios'

import { useUrlStore } from '@/stores/url_form_store';
import { storeToRefs } from "pinia";

const { url_code } = defineProps(['url_code'])
const url_store = useUrlStore()

const { id, url, url_type, slug, categories } = storeToRefs(url_store)

const emit = defineEmits(['on_save', 'on_delete'])


const save = () => {
    emit('on_save')
}

const is_correct = ref(false)
const url_list = ref([])
const categories_list = ref([])

const load_url_list = async () => {
    var r = await axios.get('/admin/list')
    url_list.value = r.data
}

const load_categories_list = async () => {
    var r = await axios.get('/admin/category/')
    categories_list.value = r.data
}

const is_url_allready_use = ref(false)
const is_slug_allready_use = ref(false)

watch(
  [url, url_type, slug],
  ([newUrl, newUrlType, newSlug], [oldUrl, oldUrlType, oldSlug]) => {
    is_correct.value = newUrl.startsWith('http') && newUrl.length > 0

    is_url_allready_use.value=false
    is_slug_allready_use.value=false

    url_list.value.forEach(url_elemnt => {
        if (url_elemnt.url === newUrl) {
            is_url_allready_use.value = true
            return
        }
        if (url_elemnt.code === newSlug){
            is_slug_allready_use.value = true
            return
        }
    })
  }
)

onMounted(load_url_list)
onMounted(load_categories_list)

</script>