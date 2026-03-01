<template>
  <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 overflow-hidden h-full pb-8">
    <!-- Left: Timeline -->
    <section class="lg:col-span-3 flex flex-col h-full overflow-hidden">
      <div class="glass-panel rounded-3xl h-full flex flex-col shadow-sm border border-white/40">
        <div class="p-6 border-b border-slate-200/30">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold tracking-widest text-primary uppercase opacity-70">TIMELINE</span>
            <span class="material-symbols-outlined text-slate-400 text-xl">calendar_month</span>
          </div>
          <h3 class="text-xl font-bold serif-font text-slate-800">时光印记</h3>
          <p class="text-xs text-slate-500 mt-1">岁月的沉淀与回响</p>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 space-y-8 relative">
          <div class="absolute left-9 top-6 bottom-6 w-px bg-gradient-to-b from-primary/20 via-slate-300/40 to-transparent"></div>
          
          <div v-for="group in timeline" :key="group.year" class="relative">
            <h4 class="text-lg font-bold text-slate-500 serif-font mb-4 pl-10" :class="{ 'text-primary': timeline[0]?.year === group.year }">{{ group.yearZh }}</h4>
            <div 
              v-for="m in group.months"
              :key="m.val"
              @click="setFilter(m.val)"
              class="relative pl-10 mb-6 group cursor-pointer hover:bg-white/20 p-2 -ml-2 rounded-xl transition-colors"
              :class="{ 'bg-white/30': activeFilter === m.val }"
            >
              <div 
                class="absolute left-[13px] top-3.5 w-2 h-2 rounded-full bg-white transition-all"
                :class="activeFilter === m.val ? 'border-2 border-primary scale-125 shadow-sm shadow-primary/30' : 'border border-slate-300 group-hover:border-primary'"
              ></div>
              <span class="text-xs font-medium block mb-1" :class="activeFilter === m.val ? 'text-primary' : 'text-slate-400'">{{ m.label }}</span>
              <p class="text-sm font-medium transition-colors" :class="activeFilter === m.val ? 'text-primary' : 'text-slate-700 group-hover:text-primary'">{{ m.count }} 篇文章</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Center: Articles List -->
    <section class="lg:col-span-5 flex flex-col h-full overflow-hidden relative">
      <div class="glass-panel rounded-3xl h-full flex flex-col shadow-lg border border-white/60 relative overflow-hidden">
        <div class="p-6 border-b border-slate-200/30 flex justify-between items-center bg-white/30 backdrop-blur-md sticky top-0 z-20">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="text-xs font-semibold tracking-widest text-primary uppercase opacity-70">ARTICLES</span>
            </div>
            <h3 class="text-xl font-bold serif-font text-slate-800">静思录</h3>
          </div>
          <div class="flex gap-2">
            <RouterLink to="/archive/gallery" class="p-2 hover:bg-white/50 rounded-lg text-slate-500 hover:text-primary transition-colors">
              <span class="material-symbols-outlined text-xl">grid_view</span>
            </RouterLink>
            <button class="p-2 bg-white/50 rounded-lg text-primary shadow-sm">
              <span class="material-symbols-outlined text-xl">view_agenda</span>
            </button>
          </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 space-y-5">
          <div v-if="loading" class="text-center text-slate-500 mt-10">加载中...</div>
          <article 
            v-for="post in filteredPosts" 
            :key="post.id"
            @click="$router.push(`/post/${post.id}`)"
            class="group relative bg-white/40 hover:bg-white/70 rounded-2xl p-6 transition-all duration-300 border border-transparent hover:border-white/50 shadow-sm hover:shadow-md cursor-pointer"
          >
            <div class="flex justify-between items-start mb-4">
              <span class="px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium">{{ post.category }}</span>
              <span class="text-xs text-slate-400 font-display">{{ post.date.replace(/-/g, '.') }}</span>
            </div>
            <h2 class="text-xl font-bold serif-font text-slate-800 mb-2 group-hover:text-primary transition-colors">{{ post.title }}</h2>
            <p class="text-sm text-slate-600 leading-relaxed line-clamp-2">{{ post.summary }}</p>
            
            <div class="mt-4 flex items-center gap-4 text-xs text-slate-400 group-hover:text-slate-500">
              <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">visibility</span> {{ formatNumber(post.views) }}</span>
              <span class="flex items-center gap-1"><span class="material-symbols-outlined text-sm">favorite</span> {{ post.likes }}</span>
              <span class="ml-auto text-primary opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">阅读全文 <span class="material-symbols-outlined text-sm">arrow_forward</span></span>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Right: Hub -->
    <section class="lg:col-span-4 flex flex-col h-full overflow-hidden">
      <div class="glass-panel rounded-3xl h-full flex flex-col shadow-sm border border-white/40">
        <div class="p-6 border-b border-slate-200/30 flex justify-between items-center">
          <div class="flex items-center gap-2 mb-2">
            <span class="text-xs font-semibold tracking-widest text-primary uppercase opacity-70">HUB</span>
            <span class="material-symbols-outlined text-slate-400 text-xl">category</span>
          </div>
          <h3 class="text-xl font-bold serif-font text-slate-800">分类与灵感</h3>
        </div>
        
        <div class="flex-1 overflow-y-auto p-4 content-start">
          <div class="grid grid-cols-2 gap-3">
            
            <div @click="toggleCategory('项目')" 
                 class="col-span-2 p-5 rounded-2xl transition-all group cursor-pointer h-32 flex flex-col justify-between"
                 :class="activeCategory === '项目' ? 'bg-indigo-50 border-indigo-400 shadow-md ring-2 ring-indigo-200/50 border' : 'bg-gradient-to-br from-indigo-50 to-white/50 border-indigo-100/50 hover:border-indigo-300/50 border'">
              <div class="flex justify-between items-start">
                <div class="p-2 bg-white rounded-lg shadow-sm text-indigo-600"><span class="material-symbols-outlined">terminal</span></div>
                <span class="text-2xl font-bold transition-colors" :class="activeCategory === '项目' ? 'text-indigo-400' : 'text-slate-300 group-hover:text-indigo-200'">01</span>
              </div>
              <div>
                <h4 class="font-bold transition-colors" :class="activeCategory === '项目' ? 'text-indigo-600' : 'text-slate-800 group-hover:text-indigo-600'">代码工程</h4>
                <p class="text-xs text-slate-500 mt-1">12 个活跃项目 · 前端探索</p>
              </div>
            </div>
            
            <div @click="toggleCategory('随笔')"
                 class="p-4 rounded-2xl transition-all group cursor-pointer h-32 flex flex-col justify-between"
                 :class="activeCategory === '随笔' ? 'bg-amber-50 border-amber-400 shadow-md ring-2 ring-amber-200/50 border' : 'bg-gradient-to-br from-amber-50 to-white/50 border-amber-100/50 hover:border-amber-300/50 border'">
              <div class="p-2 w-fit bg-white rounded-lg shadow-sm text-amber-600 mb-2"><span class="material-symbols-outlined">lightbulb</span></div>
              <div>
                <h4 class="font-bold text-sm transition-colors" :class="activeCategory === '随笔' ? 'text-amber-600' : 'text-slate-800 group-hover:text-amber-600'">奇思妙想</h4>
                <p class="text-xs text-slate-500 mt-0.5">灵感碎片</p>
              </div>
            </div>
            
            <div @click="toggleCategory('读书')"
                 class="p-4 rounded-2xl transition-all group cursor-pointer h-32 flex flex-col justify-between"
                 :class="activeCategory === '读书' ? 'bg-emerald-50 border-emerald-400 shadow-md ring-2 ring-emerald-200/50 border' : 'bg-gradient-to-br from-emerald-50 to-white/50 border-emerald-100/50 hover:border-emerald-300/50 border'">
              <div class="p-2 w-fit bg-white rounded-lg shadow-sm text-emerald-600 mb-2"><span class="material-symbols-outlined">menu_book</span></div>
              <div>
                <h4 class="font-bold text-sm transition-colors" :class="activeCategory === '读书' ? 'text-emerald-600' : 'text-slate-800 group-hover:text-emerald-600'">阅·读</h4>
                <p class="text-xs text-slate-500 mt-0.5">书单与笔记</p>
              </div>
            </div>
            
            <div @click="toggleCategory('摄影')"
                 class="col-span-2 p-4 rounded-2xl transition-all group cursor-pointer flex items-center gap-4"
                 :class="activeCategory === '摄影' ? 'bg-primary/20 border-primary shadow-sm ring-2 ring-primary/20 border' : 'bg-white/40 hover:bg-white/60 border-transparent hover:border-primary/20 border'">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center transition-colors" :class="activeCategory === '摄影' ? 'bg-primary text-white shadow-md' : 'bg-slate-200/50 text-slate-500 group-hover:text-primary group-hover:bg-primary/10'">
                <span class="material-symbols-outlined">photo_camera</span>
              </div>
              <div class="flex-1">
                <h4 class="font-bold text-sm" :class="activeCategory === '摄影' ? 'text-primary' : 'text-slate-800'">光影记录</h4>
                <p class="text-xs text-slate-500">摄影作品集</p>
              </div>
              <span class="material-symbols-outlined transition-colors" :class="activeCategory === '摄影' ? 'text-primary' : 'text-slate-300 group-hover:text-primary'">arrow_forward_ios</span>
            </div>
            
            <div @click="toggleCategory('生活')"
                 class="col-span-2 p-4 rounded-2xl transition-all group cursor-pointer flex items-center gap-4"
                 :class="activeCategory === '生活' ? 'bg-primary/20 border-primary shadow-sm ring-2 ring-primary/20 border' : 'bg-white/40 hover:bg-white/60 border-transparent hover:border-primary/20 border'">
              <div class="w-10 h-10 rounded-lg flex items-center justify-center transition-colors" :class="activeCategory === '生活' ? 'bg-primary text-white shadow-md' : 'bg-slate-200/50 text-slate-500 group-hover:text-primary group-hover:bg-primary/10'">
                <span class="material-symbols-outlined">headphones</span>
              </div>
              <div class="flex-1">
                <h4 class="font-bold text-sm" :class="activeCategory === '生活' ? 'text-primary' : 'text-slate-800'">听觉漫游</h4>
                <p class="text-xs text-slate-500">每月歌单</p>
              </div>
              <span class="material-symbols-outlined transition-colors" :class="activeCategory === '生活' ? 'text-primary' : 'text-slate-300 group-hover:text-primary'">arrow_forward_ios</span>
            </div>
            
          </div>
          
          <div class="mt-6 p-4 rounded-xl bg-primary/5 border border-primary/10 text-center">
            <p class="text-xs text-slate-500 mb-2">"保持饥饿，保持愚蠢"</p>
            <button class="text-xs font-semibold text-primary hover:underline">查看所有标签</button>
          </div>
        </div>
      </div>
    </section>

  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getPosts } from '@/api'

const posts = ref([])
const loading = ref(true)
const activeFilter = ref(null)
const activeCategory = ref(null)

const fetchPosts = async () => {
  loading.value = true
  try {
    const res = await getPosts()
    posts.value = res.data
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

const toggleCategory = (cat) => {
  activeCategory.value = activeCategory.value === cat ? null : cat
}

const formatNumber = (num) => {
  return num >= 1000 ? (num / 1000).toFixed(1) + 'k' : num.toString()
}

const filteredPosts = computed(() => {
  let result = posts.value
  if (activeCategory.value) {
    // Map visual UI categories to actual database categories
    const catMap = {
      '项目': '项目',
      '随笔': '随笔',
      '读书': '读书',
      '摄影': '光影记录', // Assuming '摄影' visually represents '光影记录' in DB based on seeding
      '生活': '生活随笔'  // Assuming '生活' translates to '听觉漫游' or similar
    }
    const dbCat = catMap[activeCategory.value] || activeCategory.value
    // Use .includes to be a bit more lenient since db categories might have suffixes like '随笔 essay'
    result = result.filter(p => p.category && p.category.includes(dbCat))
  }
  if (activeFilter.value) {
    result = result.filter(p => {
      const d = new Date(p.date)
      return `${d.getFullYear()}-${d.getMonth()+1}` === activeFilter.value
    })
  }
  return result
})

const timeline = computed(() => {
  const map = {}
  posts.value.forEach(post => {
    const d = new Date(post.date)
    const year = d.getFullYear()
    const month = d.getMonth() + 1
    const monthStr = d.toLocaleString('en-US', { month: 'short' })
    const monthZh = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][month-1] + '月'
    
    if (!map[year]) map[year] = {}
    const monthKey = `${monthZh} ${monthStr}`
    if (!map[year][monthKey]) map[year][monthKey] = { label: monthKey, val: `${year}-${month}`, count: 0 }
    map[year][monthKey].count++
  })
  
  const result = []
  const zhDigits = ['零','一','二','三','四','五','六','七','八','九']
  const toZhStr = (num) => num.toString().split('').map(d=>zhDigits[d]).join('')
  
  Object.keys(map).sort((a,b)=>b-a).forEach(y => {
    const months = []
    Object.keys(map[y]).forEach(mKey => {
       months.push(map[y][mKey])
    })
    result.push({ year: y, yearZh: '二零' + toZhStr(y.substring(2)), months })
  })
  return result
})

const setFilter = (val) => {
   if (activeFilter.value === val) activeFilter.value = null
   else activeFilter.value = val
}

onMounted(fetchPosts)
</script>
