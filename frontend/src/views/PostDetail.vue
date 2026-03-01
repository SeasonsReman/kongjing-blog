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
            <button @click="handleLike" class="w-10 h-10 rounded-full border flex items-center justify-center shadow-sm transition-all hover:scale-110" :class="isLiked ? 'bg-white border-rose-200 text-rose-500' : 'bg-white/50 border-white/60 hover:bg-white text-slate-500 hover:text-rose-500'">
              <span class="material-symbols-outlined text-xl" :class="{ 'fill-current': isLiked }">favorite</span>
            </button>
            <span class="text-xs font-display text-slate-400">{{ post.likes }}</span>
            
            <div class="w-px h-8 bg-slate-200/50 my-2"></div>
            
            <button @click="handleShare" class="w-10 h-10 rounded-full bg-white/50 border border-white/60 hover:bg-white text-slate-500 hover:text-blue-500 flex items-center justify-center shadow-sm transition-all hover:scale-110">
              <span class="material-symbols-outlined text-xl">share</span>
            </button>
            <button @click="toggleBookmark" class="w-10 h-10 rounded-full border flex items-center justify-center shadow-sm transition-all hover:scale-110" :class="isBookmarked ? 'bg-white border-primary/30 text-primary' : 'bg-white/50 border-white/60 hover:bg-white text-slate-500 hover:text-primary'">
              <span class="material-symbols-outlined text-xl" :class="{ 'fill-current': isBookmarked }">bookmark_add</span>
            </button>
          </div>

          <!-- Main Markdown Content -->
          <article class="flex-1 prose prose-slate prose-lg max-w-none prose-headings:serif-font prose-headings:font-bold prose-headings:scroll-mt-24 prose-a:text-primary prose-img:rounded-2xl prose-img:border-4 prose-img:border-white/50 prose-img:shadow-lg prose-hr:border-slate-200/50" v-html="renderedContent" ref="contentRef">
          </article>

          <!-- TOC Sidebar (Right) -->
          <div class="hidden lg:block w-48 shrink-0 relative">
            <div class="sticky top-10">
              <h4 class="text-xs font-bold tracking-widest text-slate-400 uppercase mb-4">目录</h4>
              <nav class="flex flex-col gap-3 border-l-2 border-slate-200/30 pl-4 py-1">
                <a v-for="heading in toc" :key="heading.id" :href="`#${heading.id}`" @click.prevent="scrollToHeading(heading.id)" :class="[
                  'text-sm transition-all block',
                  heading.level > 1 ? 'ml-3' : '',
                  activeHeading === heading.id ? 'font-medium text-primary border-l-2 -ml-[18px] pl-4 border-primary scale-105' : 'text-slate-500 hover:text-slate-800'
                ]">{{ heading.text }}</a>
              </nav>
              
              <!-- Author Card -->
              <div class="mt-12 p-4 bg-white/30 rounded-2xl border border-white/50 shadow-sm flex flex-col items-center text-center">
                <img src="https://api.dicebear.com/7.x/bottts-neutral/svg?seed=kongying&backgroundColor=transparent" class="w-16 h-16 rounded-full bg-[#FFBB00] border-2 border-white shadow-sm mb-3">
                <h5 class="text-sm font-bold text-slate-800 mb-1">空 · 境</h5>
                <p class="text-xs text-slate-500">记录时间的流逝与成长的轨迹。</p>
                <button @click="toggleFollow" class="mt-4 w-full py-1.5 rounded-lg text-xs font-medium transition-colors" :class="isFollowed ? 'bg-slate-200 text-slate-500' : 'bg-primary/10 text-primary hover:bg-primary/20'">{{ isFollowed ? '已关注' : '关注' }}</button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPosts, likePost } from '@/api'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const loading = ref(true)

const renderedContent = ref('')
const toc = ref([])
const activeHeading = ref('')
const contentRef = ref(null)

const isLiked = ref(false)
const isBookmarked = ref(false)
const isFollowed = ref(false)

let observer = null

const fetchPostDetail = async () => {
  loading.value = true
  try {
    const id = parseInt(route.params.id)
    const res = await getPosts()
    post.value = res.data.find(p => p.id === id) || null
    
    if (post.value) {
      // Parse markdown to HTML
      const rawHTML = marked.parse(post.value.content || '')
      
      // Extract headings for TOC by DOM parsing
      const tempDiv = document.createElement('div')
      tempDiv.innerHTML = rawHTML
      const headingElements = tempDiv.querySelectorAll('h1, h2, h3')
      const headings = []
      
      headingElements.forEach((h, index) => {
        const text = h.innerText
        const id = text.toLowerCase().replace(/[^\w\u4e00-\u9fa5]+/g, '-') || `heading-${index}`
        h.id = id // Inject ID into the HTML
        headings.push({ level: parseInt(h.tagName.substring(1)), text, id })
      })
      
      renderedContent.value = tempDiv.innerHTML
      toc.value = headings

      // Setup Scroll Spy for TOC highlighting
      nextTick(() => {
        setupScrollSpy()
      })
    }
  } catch (e) {
    console.error('Failed to load post detail', e)
  } finally {
    loading.value = false
  }
}

const handleLike = async () => {
  if (isLiked.value) return
  isLiked.value = true
  // Optimistically update the UI
  if (post.value) post.value.likes += 1
  try {
    await likePost(post.value.id)
  } catch (e) {
    console.error('Like failed', e)
  }
}

const handleShare = () => {
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    alert('✅ 文章链接已成功复制到剪贴板！')
  })
}

const toggleBookmark = () => isBookmarked.value = !isBookmarked.value
const toggleFollow = () => isFollowed.value = !isFollowed.value

const setupScrollSpy = () => {
  if (!contentRef.value) return
  if (observer) observer.disconnect()
  
  const headings = contentRef.value.querySelectorAll('h1, h2, h3')
  if (headings.length === 0) return
  
  const options = { root: null, rootMargin: '0px 0px -80% 0px', threshold: 1.0 }
  
  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) activeHeading.value = entry.target.id
    })
  }, options)
  
  headings.forEach(h => observer.observe(h))
}

const scrollToHeading = (id) => {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const formatDate = (dateStr) => {
  if(!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(fetchPostDetail)

onUnmounted(() => {
  if (observer) observer.disconnect()
})
</script>
