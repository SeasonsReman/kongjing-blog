<template>
  <main class="flex-1 p-6 flex justify-center overflow-hidden pb-8">
    <div class="w-full max-w-4xl h-full flex flex-col glass-panel rounded-3xl shadow-xl border border-white/60 relative overflow-hidden">
      
      <!-- Back button -->
      <div class="absolute top-6 left-6 z-30">
        <button @click="router.back()" class="w-10 h-10 rounded-full bg-white/40 backdrop-blur-md border border-white/50 flex items-center justify-center text-slate-700 hover:bg-white hover:text-primary transition-all shadow-sm group">
          <span class="material-symbols-outlined text-xl group-hover:-translate-x-0.5 transition-transform">arrow_back</span>
        </button>
      </div>

      <div v-if="loading" class="flex-1 flex items-center justify-center text-slate-400">
        <div class="flex flex-col items-center">
          <span class="material-symbols-outlined animate-spin text-4xl mb-3 text-primary/50">sync</span>
          <p>加载文章中...</p>
        </div>
      </div>
      
      <div v-else-if="!post" class="flex-1 flex items-center justify-center text-slate-400">
        <div class="flex flex-col items-center">
          <span class="material-symbols-outlined text-4xl mb-3 opacity-50">search_off</span>
          <p>文章不存在或已被删除</p>
          <button @click="router.push('/')" class="mt-4 px-6 py-2 bg-primary text-white rounded-full text-sm hover:bg-primary/90 transition-colors">返回首页</button>
        </div>
      </div>

      <div v-else class="flex-1 overflow-y-auto custom-scrollbar relative">
        
        <!-- Hero Section -->
        <div class="relative w-full h-[40vh] min-h-[300px] bg-slate-200">
          <div v-if="post.cover_image" class="absolute inset-0 bg-cover bg-center" :style="{ backgroundImage: `url(${post.cover_image})` }"></div>
          <div v-else class="absolute inset-0 bg-gradient-to-br from-primary/20 to-indigo-500/10"></div>
          <div class="absolute inset-0 bg-gradient-to-t from-slate-900/80 via-slate-900/20 to-transparent"></div>
          
          <div class="absolute bottom-0 left-0 w-full p-10 flex flex-col justify-end">
            <div class="flex items-center gap-3 mb-4">
              <span class="px-3 py-1 rounded-full bg-white/20 backdrop-blur-md text-white border border-white/30 text-xs font-medium tracking-wide">{{ post.category }}</span>
              <span class="text-white/80 text-sm font-display uppercase tracking-widest">{{ formatDate(post.date) }}</span>
            </div>
            <h1 class="text-4xl md:text-5xl font-bold serif-font text-white mb-2 leading-tight drop-shadow-lg">{{ post.title }}</h1>
            <p class="text-white/70 text-lg max-w-2xl line-clamp-2 drop-shadow">{{ post.summary }}</p>
          </div>
        </div>

        <!-- Content Area -->
        <div class="flex flex-col md:flex-row gap-8 p-10">
          
          <!-- Interaction Sidebar (Left) -->
          <div class="hidden md:flex flex-col gap-4 items-center w-12 sticky top-10 h-fit">
            <button class="w-10 h-10 rounded-full bg-white/50 border border-white/60 hover:bg-white text-slate-500 hover:text-rose-500 flex items-center justify-center shadow-sm transition-all hover:scale-110">
              <span class="material-symbols-outlined text-xl">favorite</span>
            </button>
            <span class="text-xs font-display text-slate-400">{{ post.likes || 12 }}</span>
            
            <div class="w-px h-8 bg-slate-200/50 my-2"></div>
            
            <button class="w-10 h-10 rounded-full bg-white/50 border border-white/60 hover:bg-white text-slate-500 hover:text-blue-500 flex items-center justify-center shadow-sm transition-all hover:scale-110">
              <span class="material-symbols-outlined text-xl">share</span>
            </button>
            <button class="w-10 h-10 rounded-full bg-white/50 border border-white/60 hover:bg-white text-slate-500 hover:text-primary flex items-center justify-center shadow-sm transition-all hover:scale-110">
              <span class="material-symbols-outlined text-xl">bookmark_add</span>
            </button>
          </div>

          <!-- Main Markdown Content -->
          <article class="flex-1 prose prose-slate prose-lg max-w-none prose-headings:serif-font prose-headings:font-bold prose-a:text-primary prose-img:rounded-2xl prose-img:border-4 prose-img:border-white/50 prose-img:shadow-lg prose-hr:border-slate-200/50">
            <!-- As a simple fallback, we just render content directly, but ideally this would use a markdown parser -->
            <div class="whitespace-pre-wrap leading-relaxed text-slate-700 font-light">{{ post.content }}</div>
          </article>

          <!-- TOC Sidebar (Right) -->
          <div class="hidden lg:block w-48 shrink-0 relative">
            <div class="sticky top-10">
              <h4 class="text-xs font-bold tracking-widest text-slate-400 uppercase mb-4">目录</h4>
              <nav class="flex flex-col gap-3 border-l-2 border-slate-200/30 pl-4 py-1">
                <a href="#" class="text-sm font-medium text-primary border-l-2 -ml-[18px] pl-4 border-primary">引言</a>
                <a href="#" class="text-sm text-slate-500 hover:text-slate-800 transition-colors">核心观点</a>
                <a href="#" class="text-sm text-slate-500 hover:text-slate-800 transition-colors">深入探索</a>
                <a href="#" class="text-sm text-slate-500 hover:text-slate-800 transition-colors">总结</a>
              </nav>
              
              <!-- Author Card -->
              <div class="mt-12 p-4 bg-white/30 rounded-2xl border border-white/50 shadow-sm flex flex-col items-center text-center">
                <img src="https://api.dicebear.com/7.x/bottts-neutral/svg?seed=kongying&backgroundColor=transparent" class="w-16 h-16 rounded-full bg-[#FFBB00] border-2 border-white shadow-sm mb-3">
                <h5 class="text-sm font-bold text-slate-800 mb-1">空 · 境</h5>
                <p class="text-xs text-slate-500">记录时间的流逝与成长的轨迹。</p>
                <button class="mt-4 w-full py-1.5 bg-primary/10 text-primary rounded-lg text-xs font-medium hover:bg-primary/20 transition-colors">关注</button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPosts } from '@/api'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const loading = ref(true)

const fetchPostDetail = async () => {
  loading.value = true
  try {
    const id = parseInt(route.params.id)
    // Note: since our backend only has getPosts, we fake fetching by ID
    const res = await getPosts()
    post.value = res.data.find(p => p.id === id) || null
  } catch (e) {
    console.error('Failed to load post detail', e)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateStr) => {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(fetchPostDetail)
</script>
