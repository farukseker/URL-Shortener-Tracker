<template>
  <section>
    <article class="my-4 flex gap-2"></article>

    <article class="my-4 flex justify-between">
      <form class="flex gap-2">
        <RouterLink class="btn btn-info text-white" :to="{ name: 'category-manage' }">
          Manage
        </RouterLink>

        <input
          class="btn btn-square"
          type="reset"
          value="×"
          @click="selected_categories_ids = []"
        />

        <input
          v-model="selected_categories_ids"
          v-for="category in categories_list"
          :key="category.id"
          :value="category.id"
          class="btn"
          type="checkbox"
          name="categories"
          :aria-label="category.name"
        />
      </form>

      <div class="flex gap-2">
        <RouterLink class="btn btn-accent" :to="{ name: 'add-url' }">
          Add
        </RouterLink>
      </div>
    </article>

    <article>
      <label class="input w-full border-0 border-b shadow outline-0" 
          :class="query_form_is_vaild ? 'outline-1 outline-error':''"
      >
        <Icon class="h-[1em] opacity-50" :icon="faSearch" />
        <input
          type="search"
          class="grow w-full"
          placeholder="Search Url & Code | Add a url"
          v-model="query"
          @keydown.enter.prevent="addNewUrl"
        />
      </label>
    </article>

    <article>
      <div class="overflow-x-auto min-h-[40vh] max-h-[80vh]">
        <table class="table table-zebra">
          <thead class="sticky top-0 z-10 bg-base-100">
            <tr>
              <th></th>
              <th class="w-1/2">Url</th>
              <th class="text-center">Code</th>
              <th class="text-center">Visit</th>
              <th class="text-center">Type</th>
              <th class="text-center">Edit</th>
              <!-- <th class="text-center">Delete</th> -->
            </tr>
          </thead>

          <tbody>
            <tr v-for="(url, index) in result_list" :key="url.code">
              <th>{{ index + 1 }}</th>

              <td class="w-1/2">
                <a
                  :href="url.url"
                  target="_blank"
                  class="font-semibold underline text-accent"
                >
                  {{ url.url?.substring(0, 80) }}
                  {{ url.url.length > 80 ? '...' : '' }}
                </a>
              </td>

              <td
                class="text-start cursor-pointer underline link-info"
                @click="copyCode(url.code)"
              >
                <span v-if="copiedCode !== url.code">
                  {{ url.code }}
                </span>

                <span
                  v-else
                  class="text-xs bg-success text-success-content px-2 py-1 rounded"
                >
                  Copied
                </span>
              </td>

              <td 
                class="text-center cursor-pointer"
                :class="url.click_count > 0 ? '' : 'text-gray-500'"
                @click="$router.push({
                  name: 'analytical-view',
                  params: {
                    url_id: url.id,
                    url_code: url.code
                  }
                })"
                >
                {{ url.click_count }} <Icon :icon="faEye" />
              </td>

              <td class="text-center">
                <div
                  v-if="url.preview_type === 'image'"
                  class="tooltip tooltip-bottom tooltip-primary"
                >
                  <div class="tooltip-content">
                    <span>image</span>
                    <img
                      class="p-1 object-contain"
                      width="200"
                      height="200"
                      :src="url.url"
                    />
                  </div>
                  <Icon :icon="faImage" />
                </div>
                <div class="tooltip tooltip-bottom tooltip-primary" data-tip="Video"><Icon v-if="url.preview_type === 'video'" :icon="faVideo" /></div> 
                <div class="tooltip tooltip-bottom tooltip-primary" data-tip="Url"><Icon v-if="url.preview_type === 'url'" :icon="faLink" /></div>
              </td>

              <td class="text-center">
                <RouterLink
                  class="btn btn-sm btn-ghost link-accent"
                  :to="{ name: 'manage-url', params: { url_code: url.code } }"
                >
                  Edit
                </RouterLink>
              </td>

              <!-- <td class="text-center">
                <button class="btn btn-sm btn-ghost link-error">
                  Delete
                </button>
              </td> -->
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </section>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed, watch } from 'vue'
import { useClipboard } from '@vueuse/core'
import { RouterLink } from 'vue-router'
import { faSearch, faImage, faVideo, faLink, faEye } from '@fortawesome/free-solid-svg-icons'
import { useUrlStore } from '@/stores/url_form_store';
import { storeToRefs } from "pinia";

const url_store = useUrlStore()
const { url } = storeToRefs(url_store)
const url_base = import.meta.env.VITE_API_URL

const url_list = ref([])
const categories_list = ref([])
const selected_categories_ids = ref([])

const query = ref('')
const query_form_is_vaild = ref(false)

const copiedCode = ref(null)
const { copy } = useClipboard()

const hasIntersection = (a, b) => {
  const setB = new Set(b)
  return a.some(x => setB.has(x))
}

const result_list = computed(() => {
  const q = query.value.toLowerCase().trim()
  const selected = selected_categories_ids.value

  return url_list.value.filter(item => {
    const text = `${item.url} ${item.code}`.toLowerCase()

    const textMatch = !q || text.includes(q)
    const categoryMatch =
      selected.length === 0 ||
      hasIntersection(selected, item.categories)

    return textMatch && categoryMatch
  })
})

watch(query, ()=>{query_form_is_vaild.value=false})

const addNewUrl = async () => {
  if (!query.value.startsWith('http')) {
    query_form_is_vaild.value = true
    return
  }

  const exists = url_list.value.some(e => e.url === query.value)

  if (exists) {
    query_form_is_vaild.value = true
    return
  }

  query_form_is_vaild.value = false
  url.value = query.value

  await url_store.create_new_url()
  url_store.flush_url_data()
  await load_url_list()
}

const copyCode = (code) => {
  copy(`${url_base}/r/${code}`)
  copiedCode.value = code
  setTimeout(() => (copiedCode.value = null), 1200)
}

const load_categories_list = async () => {
  const r = await axios.get('/admin/category/')
  categories_list.value = r.data
}

const load_url_list = async () => {
  const r = await axios.get('/admin/list')
  url_list.value = r.data
}

onMounted(async () => {
  await load_url_list()
  load_categories_list()
})
</script>
