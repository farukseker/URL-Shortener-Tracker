<template>
    <section class="h-screen">
        <header class="navbar shadow-sm">
            
            <div class="container mx-auto flex">
                <div class="flex-none">
                    <button v-if="$route.name !== 'home'" @click="$router.back" class="btn btn-square btn-ghost">
                        <Icon :icon="faChevronLeft" />
                    </button>
                    <a class="btn btn-ghost text-xl" href="/">Ulrich</a>
                </div>
                <div class="flex-1 text-center my-auto">
                    <h1 class="text-xl font-bold text-primary">{{ $route.meta.title}}</h1>
                </div>
                <div class="flex-none">
                    <details class="dropdown dropdown-end">
                        <summary class="btn btn-ghost m-1">
                            <Icon :icon="faEllipsis" />
                        </summary>
                        <ul class="menu dropdown-content bg-base-100 rounded-box z-1 min-w-100 md:min-w-52 right-0 p-2 shadow-sm">
                            <li v-if="themeStore.theme === 'dark'" @click="themeStore.set_theme('light')">Dark Mode</li>
                            <li v-if="themeStore.theme === 'light'" @click="themeStore.set_theme('dark')">Light Mode</li>
                        </ul>
                    </details>
                </div>
            </div>
        </header>
        <article class="px-4 container mx-auto">
             <RouterView />
        </article>
    </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { faEllipsis, faBars, faChevronLeft } from '@fortawesome/free-solid-svg-icons'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

onMounted(() => {
  themeStore.sync_theme()
})
</script>
