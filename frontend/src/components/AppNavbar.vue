<template>
  <header class="glass-header flex items-center justify-between px-8 py-4 mx-6 mt-6 rounded-2xl shadow-sm border border-white/40 flex-shrink-0">
    <!-- Logo -->
    <div class="flex items-center gap-3">
      <div class="flex items-center justify-center w-10 h-10 rounded-full bg-primary/10 text-primary">
        <span class="material-symbols-outlined text-2xl">{{ logoIcon }}</span>
      </div>
      <h2 class="text-xl font-bold tracking-tight serif-font text-slate-800">
        空 · 境
        <span v-if="subtitle" class="text-xs font-normal opacity-50 ml-2 tracking-wider font-display">{{ subtitle }}</span>
      </h2>
    </div>

    <!-- Nav -->
    <nav class="flex flex-1 justify-center gap-12">
      <RouterLink
        v-for="link in navLinks"
        :key="link.to"
        :to="link.to"
        class="text-slate-600 hover:text-primary text-sm font-medium transition-colors relative"
        :class="{ 'text-primary font-semibold after:content-[\'\'] after:absolute after:-bottom-1.5 after:left-1/2 after:-translate-x-1/2 after:w-1.5 after:h-1.5 after:bg-primary after:rounded-full': isActive(link) }"
      >
        {{ link.label }}
      </RouterLink>
    </nav>

    <!-- Right icons -->
    <div class="flex items-center gap-3">
      <button 
        @click="isSearchOpen = true"
        class="p-2 text-slate-500 hover:text-primary transition-colors rounded-full font-bold"
        title="搜索 (Cmd/Ctrl + K)"
      >
        <span class="material-symbols-outlined font-bold text-2xl" style="font-variation-settings: 'FILL' 0, 'wght' 600, 'GRAD' 0, 'opsz' 24;">search</span>
      </button>
      
      <NotificationDropdown />
      
      <div class="w-px h-6 bg-slate-300/50 mx-1" />
      <div class="w-10 h-10 rounded-full bg-[#FFBB00] border-2 border-white shadow-sm cursor-pointer overflow-hidden flex items-center justify-center hover:scale-105 transition-transform">
        <img src="https://api.dicebear.com/7.x/bottts-neutral/svg?seed=kongying&backgroundColor=transparent" class="w-8 h-8 object-contain" alt="User Avatar" />
      </div>
    </div>
    
    <SearchModal v-model="isSearchOpen" />
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import SearchModal from './SearchModal.vue'
import NotificationDropdown from './NotificationDropdown.vue'

const route = useRoute()
const isSearchOpen = ref(false)

const navLinks = [
  { label: '首页', to: '/' },
  { label: '归档', to: '/archive/list' },
  { label: '灵感', to: '/archive/gallery' },
  { label: '关于', to: '/about' },
]

const logoIcon = computed(() => {
  if (route.path.includes('archive')) return 'all_inclusive'
  return 'spa'
})

const subtitle = computed(() => {
  if (route.path.includes('archive')) return 'ARCHIVE'
  return ''
})

const isActive = (link) => {
  if (link.to === '/') return route.path === '/'
  return route.path === link.to
}
</script>
