<template>

<section>
  <article class="my-4 flex gap-2">

  </article>

  <article class="my-4 flex justify-between">
    <form class="flex gap-2">
      <RouterLink class="btn btn-info text-white" :to="{'name': 'category-manage'}">
        Manage
      </RouterLink>
      <input class="btn btn-square" type="reset" value="×" @click="selected_categories_ids = []" />
      <input 
          v-model="selected_categories_ids"
          v-for="(category, index) in categories_list"
          :value="category.id"
          v-bind:key="index"
          class="btn" type="checkbox" name="categories" :aria-label="category.name"/>
    </form>
    <div class="flex gap-2">
      <RouterLink class="btn btn-accent" :to="{'name': 'add-url'}">
        Add
      </RouterLink>
      <button class="btn btn-error">
        Visit
      </button>
    </div>
  </article>
  <article>
    <label class="input w-full">
      <Icon class="h-[1em] opacity-50" :icon="faSearch" />
      <input type="search" class="grow w-full" placeholder="Search" />
    </label>
  </article>
  <article>
  <div class="overflow-x-auto max-h-[80vh]">
    <table class="table table-zebra">
      <thead class="sticky top-0 z-10 bg-base-100">
        <tr>
          <th></th>
          <th class="w-1/2">Url</th>
          <th class="text-center">Code</th>
          <th class="text-center">Visit</th>
          <th class="text-center">Type</th>
          <th class="text-center">Edit</th>
          <th class="text-center">Delete</th>
        </tr>
      </thead>
      <tbody class=" w-full pb-5">
        <tr v-for="(url, index) in url_list" v-bind:key="url.code">
          <th>{{ index + 1 }}</th>
          <td class="w-1/2">
            <a :href="url.url" target="_blank" class="font-semibold underline text-accent">{{ url.url?.substring(0, 80) }}{{ url.url.length > 80 ? '...':'' }}</a>
          </td>
          <td class="text-center cursor-pointer underline" :class="url.custom ? 'link-accent':'link-neutral'"  @click="copyCode(url.code)">
            <span v-if="copiedCode !== url.code">{{ url.code }}</span>
            <span
              v-if="copiedCode === url.code"
              class="-top-6 left-1/2 -translate-x-1/2 text-xs bg-success text-success-content px-2 py-1 rounded z-20"
            >
              Copied
            </span>
          </td>
          <td class="text-center" :class="url.click_count > 0 ? 'text-current': 'text-gray-500'">{{ url.click_count }}</td>
          <td class="text-center">
            <!-- <div class="tooltip tooltip-bottom" data-tip="Image"><Icon v-if="url.preview_type === 'image'" :icon="faImage" /></div> -->
            <div class="tooltip tooltip-bottom tooltip-primary" v-if="url.preview_type === 'image'">
              <div class="tooltip-content">
                <span>image</span>
                <img class="p-1 object-contain" width="200" height="200" :src="url.url">
              </div>
              <Icon :icon="faImage" />
            </div>
            <div class="tooltip tooltip-bottom tooltip-primary" data-tip="Video"><Icon v-if="url.preview_type === 'video'" :icon="faVideo" /></div>
            <div class="tooltip tooltip-bottom tooltip-primary" data-tip="Url"><Icon v-if="url.preview_type === 'url'" :icon="faLink" /></div>
          </td>
          <td class="text-center cursor-pointer">
             <RouterLink class="btn btn-sm btn-ghost link-accent" :to="{
              name: 'manage-url', params: {url_code: url.code}
             }">
               Edit
             </RouterLink>
          </td>
          <td class="text-center">
            <button class="btn btn-sm btn-ghost link-error">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </article>
</section>

</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useClipboard } from '@vueuse/core'
import { faSearch } from '@fortawesome/free-solid-svg-icons'
import { RouterLink } from 'vue-router'
import { faImage, faVideo, faLink } from '@fortawesome/free-solid-svg-icons'

const url_base = import.meta.env.VITE_API_URL
const url_list = ref([])
const copiedCode = ref(null)
const categories_list = ref([])

const selected_categories_ids = ref([])

const { copy } = useClipboard()

const copyCode = (code) => {
  copy(`${url_base}/r/${code}`)
  copiedCode.value = code
  setTimeout(() => {
    copiedCode.value = null
  }, 1200)
}

const load_categories_list = async () => {
    var r = await axios.get('/admin/category/')
    categories_list.value = r.data
}

onMounted(async () => {
  const r = await axios.get('/admin/list')
  url_list.value = r.data
  load_categories_list()
})
</script>
