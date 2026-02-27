<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="modelValue" class="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh]">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm" @click="close"></div>
        
        <!-- Modal -->
        <div class="relative w-full max-w-2xl mx-4 bg-white/70 backdrop-blur-2xl rounded-3xl shadow-2xl border border-white overflow-hidden flex flex-col max-h-[70vh]">
          
          <!-- Search Input -->
          <div class="flex items-center px-6 py-4 border-b border-white/40 bg-white/40">
            <span class="material-symbols-outlined text-primary text-2xl mr-3">search</span>
            <input 
              v-model="searchQuery"
              ref="searchInput"
              type="text" 
              class="flex-1 bg-transparent border-none outline-none text-slate-800 text-lg placeholder:text-slate-400 font-medium"
              placeholder="搜索文章、灵感、任务..."
              @keydown.esc="close"
            >
            <button class="bg-slate-200/50 hover:bg-slate-200 text-slate-500 text-xs px-2 py-1 rounded transition-colors font-mono tracking-widest" @click="close">
              ESC
            </button>
          </div>

          <!-- Results Layout -->
          <div class="flex-1 overflow-y-auto p-4 custom-scrollbar">
            
            <div v-if="!searchQuery" class="text-center py-12 text-slate-400">
              <span class="material-symbols-outlined text-4xl mb-3 opacity-50">travel_explore</span>
              <p class="text-sm">输入关键词开始搜索</p>
            </div>

            <div v-else-if="isLoading" class="text-center py-12 text-slate-400">
              <span class="material-symbols-outlined animate-spin text-3xl mb-2 text-primary">hourglass_empty</span>
              <p class="text-sm">检索中...</p>
            </div>

            <div v-else-if="!hasResults" class="text-center py-12 text-slate-400">
              <span class="material-symbols-outlined text-4xl mb-3 opacity-50">search_off</span>
              <p class="text-sm text-slate-500">未找到跟 "<span class="text-primary font-medium">{{ searchQuery }}</span>" 相关的结果</p>
            </div>

            <div v-else class="space-y-6">
              <!-- Posts Results -->
              <div v-if="results.posts.length > 0">
                <h4 class="text-xs font-bold tracking-widest text-primary/70 uppercase mb-3 px-2">文章</h4>
                <div class="space-y-1">
                  <div v-for="post in results.posts" :key="post.id" @click="handleSelect(post.id, 'post')" class="p-3 hover:bg-white/50 rounded-xl cursor-pointer transition-colors group flex items-start gap-4">
                    <div class="w-10 h-10 rounded-lg bg-primary/5 flex items-center justify-center flex-shrink-0 text-primary group-hover:bg-primary/10">
                      <span class="material-symbols-outlined">article</span>
                    </div>
                    <div>
                      <h5 class="text-sm font-semibold text-slate-800 group-hover:text-primary transition-colors">{{ post.title }}</h5>
                      <p class="text-xs text-slate-500 mt-1 line-clamp-1">{{ post.summary }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Notes Results -->
              <div v-if="results.notes.length > 0">
                <h4 class="text-xs font-bold tracking-widest text-primary/70 uppercase mb-3 px-2">灵感</h4>
                <div class="space-y-1">
                  <div v-for="note in results.notes" :key="note.id" @click="handleSelect(note.id, 'note')" class="p-3 hover:bg-white/50 rounded-xl cursor-pointer transition-colors group flex items-start gap-4">
                     <div class="w-10 h-10 rounded-lg bg-amber-500/5 flex items-center justify-center flex-shrink-0 text-amber-500 group-hover:bg-amber-500/10">
                      <span class="material-symbols-outlined">lightbulb</span>
                    </div>
                    <div class="flex-1">
                      <p class="text-sm text-slate-700 font-medium line-clamp-2">{{ note.content }}</p>
                      <span class="text-[10px] text-slate-400 mt-1 block">{{ new Date(note.created_at).toLocaleString('en-US',{month:'short',day:'numeric'}) }}</span>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPosts, getNotes } from '@/api'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])
const router = useRouter()

const searchInput = ref(null)
const searchQuery = ref('')
const isLoading = ref(false)
const results = ref({ posts: [], notes: [] })

const hasResults = computed(() => results.value.posts.length > 0 || results.value.notes.length > 0)
import { computed } from 'vue'

const close = () => {
  emit('update:modelValue', false)
  searchQuery.value = ''
  results.value = { posts: [], notes: [] }
}

const performSearch = async (query) => {
  if (!query.trim()) {
    results.value = { posts: [], notes: [] }
    return
  }
  
  isLoading.value = true
  try {
    const q = query.toLowerCase()
    const [postsRes, notesRes] = await Promise.all([getPosts(), getNotes()])
    
    // Fuzzy search
    const matchedPosts = postsRes.data.filter(p => p.title.toLowerCase().includes(q) || p.summary?.toLowerCase().includes(q) || p.content?.toLowerCase().includes(q))
    const matchedNotes = notesRes.data.filter(n => n.content.toLowerCase().includes(q))
    
    results.value = {
      posts: matchedPosts.slice(0, 5),
      notes: matchedNotes.slice(0, 5)
    }
  } catch (e) {
    console.error("Search failed", e)
  } finally {
    isLoading.value = false
  }
}

let debounceTimer = null
watch(searchQuery, (newVal) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => performSearch(newVal), 300)
})

watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    nextTick(() => {
      searchInput.value?.focus()
    })
  }
})

const handleSelect = (id, type) => {
  close()
  if (type === 'post') {
    // Navigate to post detail when ready, for now gallery
    router.push(`/post/${id}`).catch(() => router.push('/archive/gallery'))
  } else if (type === 'note') {
    router.push('/')
  }
}

const handleKeydown = (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault()
    emit('update:modelValue', true)
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active .relative {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.fade-enter-from .relative {
  opacity: 0;
  transform: translateY(-20px) scale(0.98);
}
</style>
