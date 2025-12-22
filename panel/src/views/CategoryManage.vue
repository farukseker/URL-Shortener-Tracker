<template>
  <section class="w-full my-4 flex">
    <article class="justify-center m-auto w-2/3">
      <label class="input w-full outline-0">
        <Icon class="h-[1em] opacity-50" :icon="faSearch" />
        <input
          type="search"
          class="grow"
          placeholder="Search & Add"
          v-model="query"
          @keydown.enter.prevent="addCategory"
        />
      </label>

      <div class="overflow-x-auto max-h-[80vh]">
        <table class="table table-zebra">
          <thead class="sticky top-0 z-10 bg-base-100">
            <tr>
              <th></th>
              <th class="w-1/2">Category</th>
              <th class="text-center">Delete</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="(category, index) in filteredCategories"
              :key="category.id"
            >
              <th>{{ index + 1 }}</th>

              <th
                class="w-1/2"
                contenteditable
                @blur="updateCategory($event, category)"
              >
                {{ category.name }}
              </th>

              <th class="text-center">
                <button @click="deleteCategory(category.id)">
                  Delete
                </button>
              </th>
            </tr>
          </tbody>
        </table>
      </div>
    </article>
  </section>
</template>

<script setup>
import axios from "axios";
import { ref, computed, onMounted } from "vue";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import slugify from "slugify";

const query = ref("");
const categories_list = ref([]);

const filteredCategories = computed(() => {
  if (!query.value) return categories_list.value;
  return categories_list.value.filter(c =>
    c.name.toLowerCase().includes(query.value.toLowerCase())
  )
})


const loadCategories = async () => {
  const r = await axios.get("/admin/category/");
  categories_list.value = r.data;
};

const addCategory = async () => {
  if (!query.value.trim()) return;

  await axios.post("/admin/category/", null, {
    params: {
      name: query.value,
      slug: slugify(query.value, { lower: true })
    }
  })

  query.value = "";

  await loadCategories()
}

const updateCategory = async (e, category) => {
    const newName = e.target.innerText.trim();
    if (newName === category.name) return;

    axios.put(`/admin/category/${category.id}`, null, {
        params: {
            name: newName,
            slug: slugify(newName, { lower: true })
        }
    })
    category.name = newName;
}


const deleteCategory = async id => {
    await axios.delete(`/admin/category/${id}`, {
        params: { id }
    })
    await loadCategories()
}

onMounted(loadCategories);
</script>

