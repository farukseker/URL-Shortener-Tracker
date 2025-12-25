import { defineStore } from 'pinia'
import type { Ref } from 'vue'
import { ref, toRaw } from 'vue'
import axios from 'axios'

type Category = {
    id: number
    name: string
    slug: string
}

export const useUrlStore = defineStore('url_store', () => {
    const id: Ref<String | null> = ref(null)
    const url: Ref<String | null> = ref(null)
    const url_type: Ref<String | null> = ref(null)
    const slug: Ref<String | null> = ref(null)
    // const categories: Ref<List[]> = ref([])
    const categories = ref<[]>([])

    const create_new_url = async (): Promise<Object> => {
        console.log(categories.value)
        const r = await axios.post('/admin/create', {
            long_url: url.value,
            preview_type: url_type.value,
            custom_code: slug.value,
            categories: categories.value
            // categories: categories.value.map(c => ({
            //     id: c.id,
            //     name: c.name,
            // })),
        })
        return r.data

    }

    const update_url = async (): Promise<void> => {
        await axios.post('/admin/create', {
            id: id.value,
            long_url: url.value,
            preview_type: url_type.value,
            custom_code: slug.value,
            categories: toRaw(categories.value),
        })
    }

    const save_url = async (): Promise<void> => {
        const func = id?.value ? update_url : create_new_url
        await func()
    }

    const get_url = async (code: String): Promise<Object> => {
        var r = await axios.get(`/admin/url`, {params: {code: code}})
        // r.data.categories = r.data.categories?.forEach(e => {return e.id})
        return r.data
    }

    const delete_url = async (code: String) => {
        await axios.delete(`/admin/url`, {params: {code: code}})
    }
    
    const load_url_data = (payload: Object): void => {
        id.value = payload.hasOwnProperty('id') ? payload.id : null
        url.value = payload.hasOwnProperty('url') ? payload.url : null
        url_type.value = payload.hasOwnProperty('url_type') ? payload.url_type : null
        slug.value = payload.hasOwnProperty('code') ? payload.code : null
        categories.value = payload.hasOwnProperty('categories') ? payload.categories : []
    }

    const flush_url_data = () => {
        id.value = null
        url.value = null
        url_type.value = null
        slug.value = null
        categories.value = []
    }

    return { 
        id, url, url_type, slug, categories,
        create_new_url, update_url, save_url, get_url, delete_url, load_url_data, flush_url_data
    }
})
