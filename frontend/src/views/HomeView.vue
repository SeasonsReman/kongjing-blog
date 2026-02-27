<template>
  <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-6 overflow-hidden pb-8">

    <!-- Left: Timeline / Tasks -->
    <section class="lg:col-span-3 flex flex-col h-full overflow-hidden">
      <div class="glass-panel rounded-3xl h-full flex flex-col shadow-sm border border-white/40">
        <div class="p-6 border-b border-slate-200/30">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold tracking-widest text-primary uppercase opacity-70">TIMELINE</span>
            <span class="material-symbols-outlined text-slate-400 text-xl">history_edu</span>
          </div>
          <h3 class="text-xl font-bold serif-font text-slate-800">日落跌进昭昭星野</h3>
          <p class="text-xs text-slate-500 mt-1">记录时间的流逝与成长的轨迹</p>
        </div>

        <div class="flex-1 overflow-y-auto p-6 space-y-5">
          <div v-if="loadingTasks" class="text-center text-slate-400 text-sm pt-4">加载中…</div>
          <div
            v-for="task in tasks"
            :key="task.id"
            class="relative pl-6 border-l border-slate-200/60 group"
          >
            <div
              class="absolute -left-[5px] top-1.5 w-[9px] h-[9px] rounded-full bg-white border-2 transition-colors"
              :class="task.done ? 'border-slate-300' : 'border-primary ring-4 ring-primary/5'"
            />
            <div class="flex flex-col gap-0.5">
              <span v-if="!task.done" class="text-xs font-medium text-primary bg-primary/10 px-2 py-0.5 rounded w-fit">进行中</span>
              <span v-else class="text-xs font-medium text-slate-400 bg-slate-100/60 px-2 py-0.5 rounded w-fit">已完成</span>
              <h4 class="text-sm font-semibold text-slate-800 mt-1 line-clamp-1">{{ task.title }}</h4>
              <p class="text-xs text-slate-500">{{ task.tag }}</p>
            </div>
          </div>
          <div v-if="!loadingTasks && tasks.length === 0" class="text-center text-slate-400 text-sm pt-4">暂无任务</div>
        </div>
      </div>
    </section>

    <!-- Middle: Inspiration capture -->
    <section class="lg:col-span-5 flex flex-col h-full overflow-hidden">
      <div class="glass-panel rounded-3xl h-full flex flex-col shadow-lg border border-white/60 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary/30 via-primary to-primary/30" />

        <div class="p-8 flex-1 flex flex-col items-center justify-center text-center">
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-white to-white/50 shadow-inner flex items-center justify-center mb-6">
            <span class="material-symbols-outlined text-primary text-4xl">auto_awesome</span>
          </div>
          <h1 class="text-3xl font-bold serif-font text-slate-900 mb-3">捕捉此刻的灵感</h1>
          <p class="text-slate-600 max-w-md mx-auto mb-8 font-light">
            让思绪如云般自由流淌，记录下每一个闪光的瞬间。
          </p>

          <div class="w-full max-w-md bg-white/60 backdrop-blur-md rounded-2xl p-2 shadow-inner border border-white/50 transition-all focus-within:ring-2 focus-within:ring-primary/20 focus-within:bg-white/80">
            <textarea
              v-model="noteText"
              class="w-full bg-transparent border-0 p-4 text-slate-800 placeholder:text-slate-400 focus:ring-0 resize-none h-32 text-base leading-relaxed"
              placeholder="在此输入..."
            />
            <div class="flex items-center justify-between px-2 pb-2">
              <div class="flex gap-2">
                <button class="p-2 hover:bg-slate-200/50 rounded-lg text-slate-500 transition-colors">
                  <span class="material-symbols-outlined text-xl">image</span>
                </button>
                <button class="p-2 hover:bg-slate-200/50 rounded-lg text-slate-500 transition-colors">
                  <span class="material-symbols-outlined text-xl">mic</span>
                </button>
              </div>
              <button
                @click="saveNote"
                :disabled="!noteText.trim()"
                class="bg-primary hover:bg-primary/90 disabled:opacity-40 text-white px-6 py-2 rounded-xl text-sm font-medium shadow-lg shadow-primary/30 transition-all hover:scale-[1.02] active:scale-[0.98]"
              >
                记录
              </button>
            </div>
          </div>

          <div v-if="savedMsg" class="mt-4 text-sm text-primary font-medium animate-pulse">✨ 已保存！</div>
        </div>

        <!-- Today's quote & Recent Notes -->
        <div class="flex-1 min-h-[35%] overflow-y-auto bg-white/20 border-t border-white/20 backdrop-blur-sm p-6 custom-scrollbar">
          <div class="flex gap-4 items-start mb-6 w-full">
            <span class="material-symbols-outlined text-primary/60">format_quote</span>
            <div>
              <p class="serif-font text-slate-700 italic text-sm">{{ currentQuote.text }}</p>
              <p class="text-xs text-slate-500 mt-1">— {{ currentQuote.author }}</p>
            </div>
          </div>
          
          <div v-if="notes.length > 0" class="pt-2 border-t border-white/30">
            <h4 class="text-[10px] font-bold tracking-widest text-slate-400 uppercase mb-3">RECENT INSPIRATIONS</h4>
            <div class="space-y-3 pb-2">
              <div v-for="note in notes" :key="note.id" class="p-4 rounded-2xl bg-white/40 border border-white/50 text-sm text-slate-700 shadow-sm text-left hover:bg-white/60 transition-colors group">
                <p class="leading-relaxed whitespace-pre-wrap">{{ note.content }}</p>
                <div class="flex justify-between items-center mt-3">
                   <span class="text-[10px] text-slate-400 font-display uppercase">{{ new Date(note.created_at).toLocaleString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}) }}</span>
                   <div class="flex items-center gap-2">
                     <button @click="saveNoteToGallery(note)" class="text-slate-400 hover:text-primary transition-colors opacity-0 group-hover:opacity-100 tooltip" title="转存至灵感画廊"><span class="material-symbols-outlined text-sm">bookmark_add</span></button>
                     <button @click="handleRemoveNote(note.id)" class="text-slate-400 hover:text-red-400 transition-colors opacity-0 group-hover:opacity-100 tooltip" title="删除"><span class="material-symbols-outlined text-sm">delete</span></button>
                   </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Right: Focus / Today's tasks -->
    <section class="lg:col-span-4 flex flex-col h-full overflow-hidden">
      <div class="glass-panel rounded-3xl h-full flex flex-col shadow-sm border border-white/40">
        <div class="p-6 border-b border-slate-200/30 flex justify-between items-center">
          <div>
            <span class="text-xs font-semibold tracking-widest text-primary uppercase opacity-70">FOCUS</span>
            <h3 class="text-xl font-bold serif-font text-slate-800 mt-1">今日专注</h3>
          </div>
          <div class="bg-white/40 rounded-lg px-3 py-1.5 backdrop-blur-sm">
            <span class="text-xs font-bold text-slate-700">{{ pendingCount }} 项待办</span>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-3">
          <label
            v-for="task in tasks"
            :key="task.id"
            class="flex items-center p-4 bg-white/40 hover:bg-white/60 rounded-xl cursor-pointer group transition-all border border-transparent hover:border-primary/20"
          >
            <div class="relative flex items-center flex-shrink-0">
              <input
                type="checkbox"
                :checked="task.done"
                @change="toggleTask(task)"
                class="peer h-5 w-5 cursor-pointer appearance-none rounded-md border-2 border-slate-300 transition-all checked:border-primary checked:bg-primary hover:border-primary focus:ring-0"
              />
              <span class="material-symbols-outlined absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-sm text-white opacity-0 peer-checked:opacity-100 pointer-events-none">check</span>
            </div>
            <div class="ml-4 flex-1 min-w-0">
              <p class="text-sm font-medium text-slate-800 group-hover:text-primary transition-colors" :class="{ 'line-through opacity-50': task.done }">{{ task.title }}</p>
              <p class="text-xs text-slate-500 mt-0.5">{{ task.priority }} • {{ task.tag }}</p>
            </div>
            <button
              @click.prevent="removeTask(task.id)"
              class="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:text-red-400 text-slate-400 ml-2"
            >
              <span class="material-symbols-outlined text-base">close</span>
            </button>
          </label>
        </div>

        <!-- Add new task -->
        <div class="p-4 border-t border-slate-200/30">
          <div v-if="addingTask" class="flex gap-2 mb-3">
            <input
              v-model="newTaskTitle"
              @keydown.enter="addTask"
              class="flex-1 bg-white/60 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-primary"
              placeholder="任务名称…"
            />
            <input
              v-model="newTaskTag"
              @keydown.enter="addTask"
              class="w-20 bg-white/60 border border-slate-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-primary"
              placeholder="标签"
            />
            <button @click="addTask" class="bg-primary text-white rounded-xl px-3 py-2 text-sm">✓</button>
          </div>
          <button
            @click="addingTask = !addingTask"
            class="w-full flex items-center justify-center gap-2 p-3 rounded-xl border border-dashed border-slate-400/50 text-slate-500 hover:text-primary hover:border-primary/50 hover:bg-primary/5 transition-all text-sm font-medium"
          >
            <span class="material-symbols-outlined text-lg">{{ addingTask ? 'expand_less' : 'add' }}</span>
            {{ addingTask ? '收起' : '添加新任务' }}
          </button>
        </div>
      </div>
    </section>

  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getTasks, createTask, updateTask, deleteTask, createNote, getNotes, deleteNote, createPost } from '@/api'

const tasks = ref([])
const loadingTasks = ref(true)
const noteText = ref('')
const savedMsg = ref(false)
const addingTask = ref(false)
const newTaskTitle = ref('')
const newTaskTag = ref('')
const notes = ref([])

const pendingCount = computed(() => tasks.value.filter(t => !t.done).length)

const quotes = [
  { text: "Simplicity is the ultimate sophistication.", author: "Leonardo da Vinci" },
  { text: "少即是多。", author: "密斯·凡·德·罗" },
  { text: "最好的设计是无感知的设计。", author: "佚名" },
  { text: "保持饥饿，保持愚蠢。", author: "Steve Jobs" },
]
const currentQuote = computed(() => quotes[new Date().getDay() % quotes.length])

const fetchTasks = async () => {
  try {
    const res = await getTasks()
    tasks.value = res.data.map(t => ({ ...t, done: Boolean(t.done) }))
  } catch (e) { console.error(e) }
  finally { loadingTasks.value = false }
}

const toggleTask = async (task) => {
  const newDone = !task.done
  task.done = newDone
  await updateTask(task.id, { done: newDone })
}

const removeTask = async (id) => {
  await deleteTask(id)
  tasks.value = tasks.value.filter(t => t.id !== id)
}

const addTask = async () => {
  if (!newTaskTitle.value.trim()) return
  const res = await createTask({ title: newTaskTitle.value.trim(), tag: newTaskTag.value.trim() || '其他' })
  tasks.value.push({ ...res.data, done: false })
  newTaskTitle.value = ''
  newTaskTag.value = ''
  addingTask.value = false
}

const saveNote = async () => {
  if (!noteText.value.trim()) return
  const res = await createNote({ content: noteText.value.trim() })
  notes.value.unshift(res.data)
  noteText.value = ''
  savedMsg.value = true
  setTimeout(() => savedMsg.value = false, 2500)
}

const fetchNotes = async () => {
  try {
    const res = await getNotes()
    notes.value = res.data.slice(0, 10) // show up to 10 recent
  } catch (e) { console.error(e) }
}

const handleRemoveNote = async (id) => {
  await deleteNote(id)
  notes.value = notes.value.filter(n => n.id !== id)
}

const saveNoteToGallery = async (note) => {
  try {
    const sumText = note.content.length > 50 ? note.content.substring(0, 50) + '...' : note.content
    const postData = {
      title: '灵感捕捉',
      summary: sumText,
      content: note.content,
      category: '随笔',
      mood: 'Inspired'
    }
    await createPost(postData)
    // Optional: remove note after transferring or just show toast
    await handleRemoveNote(note.id)
    savedMsg.value = true
    setTimeout(() => { savedMsg.value = false }, 2500)
  } catch (e) {
    console.error('Save to gallery failed', e)
  }
}

onMounted(() => {
  fetchTasks()
  fetchNotes()
})
</script>
