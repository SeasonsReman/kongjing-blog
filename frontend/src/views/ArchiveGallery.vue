<template>
  <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-8 overflow-hidden pb-8">

    <!-- Articles Feed -->
    <section class="lg:col-span-9 flex flex-col h-full overflow-hidden">
      <div class="glass-panel rounded-3xl h-full flex flex-col shadow-lg border border-white/60 relative overflow-hidden">
        <div class="p-6 border-b border-white/20 flex justify-between items-center bg-white/20 backdrop-blur-xl z-20 shadow-[0_4px_30px_rgba(0,0,0,0.03)]">
          <div>
            <h3 class="text-2xl font-bold serif-font bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-500">记忆画廊 <span class="text-xs font-normal text-slate-400 ml-2 font-display tracking-widest uppercase">Collecting moments, not things.</span></h3>
          </div>
          <div class="flex gap-2">
            <button class="p-2 bg-white/50 rounded-lg text-primary shadow-sm">
              <span class="material-symbols-outlined text-xl">grid_view</span>
            </button>
            <RouterLink to="/archive/list" class="p-2 hover:bg-white/50 rounded-lg text-slate-500 hover:text-primary transition-colors">
              <span class="material-symbols-outlined text-xl">view_list</span>
            </RouterLink>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          <div v-if="loading" class="text-center text-slate-500 mt-10">加载中...</div>
          
          <div v-else class="columns-1 md:columns-2 lg:columns-3 gap-6 space-y-6">
            <article 
              v-for="(post, index) in filteredPosts" 
              :key="post.id"
              @click="handlePostClick(post)"
              class="break-inside-avoid relative bg-white/20 backdrop-blur-lg rounded-[2rem] p-6 transition-all duration-500 border border-white/40 hover:border-white/80 hover:bg-white/40 hover:-translate-y-2 hover:shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05),0_0_30px_rgba(255,255,255,0.6)] cursor-pointer group flex flex-col overflow-hidden animate-fade-in-up w-full"
              :style="{ animationDelay: `${index * 0.05}s`, animationFillMode: 'both' }"
            >
              <!-- Subtle internal glow on hover -->
              <div class="absolute inset-0 bg-gradient-to-br from-white/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-[2rem] pointer-events-none"></div>

              <div class="flex justify-between items-start mb-5 relative z-10">
                <span class="text-[10px] text-slate-400 font-display uppercase tracking-widest font-semibold">{{ formatDate(post.date) }}</span>
                <span class="px-4 py-1.5 rounded-full bg-white/50 backdrop-blur-md text-slate-600 border border-white shadow-sm text-xs font-medium tracking-wide">{{ post.mood }}</span>
              </div>
              
              <h2 class="text-2xl font-bold serif-font text-slate-800 mb-3 group-hover:text-primary transition-colors relative z-10 leading-snug">{{ post.title }}</h2>
              <p class="text-sm text-slate-600 leading-relaxed line-clamp-2 mb-5 flex-1 relative z-10 font-light">
                {{ post.summary }}
              </p>
              
              <!-- Dynamic aspect ratio cover images based on abstract image width/height (masonry simulation) -->
              <div v-if="post.cover_image" class="w-full rounded-2xl overflow-hidden mb-5 bg-slate-200/50 border border-white/30 relative z-10 shadow-inner group-hover:shadow-[0_0_20px_rgba(255,255,255,0.3)]"
                   :class="post.category === '摄影' ? 'h-64' : 'h-40'">
                <div class="w-full h-full bg-cover bg-center transition-transform duration-700 ease-out group-hover:scale-[1.15]" 
                     :style="{ backgroundImage: `url(${post.cover_image})` }">
                     
                  <!-- Lightbox Hover Indicator for Photography -->
                  <div v-if="post.category === '摄影'" class="absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/20 transition-colors flex items-center justify-center opacity-0 group-hover:opacity-100 duration-500 backdrop-blur-sm">
                    <span class="material-symbols-outlined text-white text-4xl drop-shadow-lg scale-50 group-hover:scale-100 transition-transform duration-500 ease-out">zoom_in</span>
                  </div>
                </div>
              </div>
              
              <div class="flex items-center justify-between text-xs text-slate-400 mt-auto relative z-20">
                <span class="flex items-center gap-1.5 font-medium"><span class="material-symbols-outlined text-[14px]">schedule</span> 5 min read</span>
                <button @click.prevent="handleDeletePost(post.id)" class="opacity-0 group-hover:opacity-100 transition-all duration-300 p-1.5 text-slate-400 hover:text-red-500 hover:bg-white/80 rounded-lg text-xs gap-1 flex items-center shadow-sm">
                  <span class="material-symbols-outlined text-[14px]">delete</span>
                </button>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>

    <!-- Right Sidebar: Moods & Categories -->
    <section class="lg:col-span-3 flex flex-col h-full overflow-hidden space-y-6">
      <!-- MOODS -->
      <div class="glass-panel flex-1 min-h-[50%] h-1/2 rounded-3xl p-6 shadow-sm border border-white/40 flex flex-col overflow-hidden">
        <div class="flex items-center gap-2 mb-6 shrink-0">
          <span class="material-symbols-outlined text-primary">psychology</span>
          <span class="text-xs font-semibold tracking-widest text-slate-600 uppercase">MOODS</span>
        </div>
        
        <div class="flex flex-col gap-3 overflow-y-auto custom-scrollbar pr-2 pb-4">
          <button 
            v-for="mood in moods" 
            :key="mood.name"
            @click="toggleMood(mood.name)"
            class="flex items-center gap-3 px-5 py-2.5 rounded-full w-fit transition-all duration-300 text-sm font-medium shadow-sm"
            :class="activeMood === mood.name ? 'bg-white/80 text-primary border border-white shadow-[0_0_15px_rgba(255,255,255,0.8)] scale-105' : 'bg-white/20 text-slate-600 hover:bg-white/50 border border-white/30 hover:shadow-md'"
          >
            <div class="w-2 h-2 rounded-full transition-colors duration-300" :class="activeMood === mood.name ? 'bg-primary shadow-[0_0_8px_rgba(76,49,211,0.6)]' : 'bg-slate-300'"></div>
            {{ mood.name }}
          </button>
        </div>
      </div>

      <!-- CATEGORIES -->
      <div class="glass-panel flex-1 min-h-[50%] h-1/2 rounded-3xl p-6 shadow-sm border border-white/40 flex flex-col overflow-hidden">
        <div class="flex items-center gap-2 mb-6 shrink-0">
          <span class="text-xs font-semibold tracking-widest text-slate-600 uppercase">CATEGORIES</span>
        </div>
        
        <div class="space-y-3 overflow-y-auto custom-scrollbar pr-2 pb-4">
          <div 
            class="flex justify-between items-center text-sm group cursor-pointer px-3 py-2 rounded-xl transition-all duration-300" 
            :class="activeCategory === cat.name ? 'bg-primary/10 border border-primary/20 shadow-sm' : 'hover:bg-white/40 border border-transparent'"
            v-for="cat in categories" 
            :key="cat.name"
            @click="toggleCategory(cat.name)"
          >
            <span class="serif-font transition-colors flex items-center gap-2" :class="activeCategory === cat.name ? 'text-primary font-bold' : 'text-slate-600 group-hover:text-primary'">
              {{ cat.name }} <span class="font-display opacity-50" :class="activeCategory === cat.name ? 'text-primary' : ''">{{ cat.en }}</span>
            </span>
            <span class="text-xs font-display px-2 py-0.5 rounded" :class="activeCategory === cat.name ? 'bg-primary border border-primary text-white shadow-sm' : 'bg-white/50 text-slate-400 group-hover:bg-white'">{{ cat.count }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Lightbox Component -->
    <Lightbox 
      v-model="isLightboxOpen" 
      :images="lightboxImages" 
      v-model:currentIndex="lightboxIndex" 
    />
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getPosts, deletePost } from '@/api'
import Lightbox from '@/components/Lightbox.vue'

const router = useRouter()
const posts = ref([])
const loading = ref(true)
const activeMood = ref(null)
const activeCategory = ref(null)

const moods = [
  { name: 'Calm' }, { name: 'Inspired' }, { name: 'Deep' },
  { name: 'Melancholy' }, { name: 'Journey' }, { name: 'Tech' }
]

const categories = [
  { name: '随笔', en: 'essay', count: 12 },
  { name: '摄影', en: 'photography', count: 8 },
  { name: '项目', en: 'project', count: 3 },
  { name: '读书', en: 'reading', count: 5 },
  { name: '生活', en: 'life', count: 21 },
]

const fetchPosts = async () => {
  loading.value = true
  try {
    // Fetch ALL posts once, filter locally for speed and smooth transitions
    const res = await getPosts()
    posts.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const filteredPosts = computed(() => {
  let result = posts.value
  
  if (activeMood.value) {
    result = result.filter(p => p.mood === activeMood.value)
  }
  
  if (activeCategory.value) {
    // Exact match for the left name in the categories array
    const targetCat = activeCategory.value
    result = result.filter(p => p.category && p.category.includes(targetCat))
  }
  
  return result
})

const toggleMood = (mood) => {
  activeMood.value = activeMood.value === mood ? null : mood
}

const toggleCategory = (cat) => {
  activeCategory.value = activeCategory.value === cat ? null : cat
}

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  const month = d.toLocaleString('en-US', { month: 'short' }).toUpperCase()
  const day = d.getDate().toString().padStart(2, '0')
  return `${month} ${day}`
}

const isLightboxOpen = ref(false)
const lightboxIndex = ref(0)
const lightboxImages = ref([])

const handlePostClick = (post) => {
  if (post.category === '摄影' && post.cover_image) {
    // Collect all photography images in current view
    const photos = posts.value.filter(p => p.category === '摄影' && p.cover_image)
    lightboxImages.value = photos.map(p => ({
      url: p.cover_image,
      caption: p.title,
      info: formatDate(p.date)
    }))
    // Find index of clicked photo
    lightboxIndex.value = photos.findIndex(p => p.id === post.id)
    isLightboxOpen.value = true
  } else {
    // Normal routing to post detail
    router.push(`/post/${post.id}`)
  }
}

const handleDeletePost = async (id) => {
  if (confirm('确定要删除这条记录吗？')) {
    try {
      await deletePost(id)
      posts.value = posts.value.filter(p => p.id !== id)
    } catch (e) {
      console.error('Failed to delete post', e)
    }
  }
}

onMounted(fetchPosts)
</script>

<style scoped>
@keyframes fade-in-up {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
</style>
