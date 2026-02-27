<template>
  <div class="relative" ref="dropdownRef">
    <!-- Trigger Button -->
    <button 
      @click="toggle"
      class="relative flex items-center justify-center w-10 h-10 text-[#4c31d3] transition-all duration-300 rounded-full bg-white shadow-sm border border-slate-100 hover:shadow-md hover:scale-105"
      :class="{ 'ring-4 ring-[#4c31d3]/10': isOpen }"
    >
      <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 0, 'wght' 500, 'GRAD' 0, 'opsz' 24;">
        notifications
      </span>
      <span v-if="unreadCount > 0" class="absolute top-[8px] right-[8px] w-[9px] h-[9px] bg-[#0084ff] border-2 border-white rounded-full"></span>
    </button>

    <!-- Dropdown Panel -->
    <Transition name="dropdown">
      <div v-if="isOpen" class="absolute right-0 mt-3 w-80 bg-white/70 backdrop-blur-2xl rounded-2xl shadow-xl border border-white/60 overflow-hidden z-50 flex flex-col max-h-[400px]">
        <div class="p-4 border-b border-white/40 flex justify-between items-center bg-white/40">
          <h4 class="font-bold text-slate-800 text-sm">通知中心</h4>
          <button @click="markAllRead" class="text-xs text-primary font-medium hover:underline">全部已读</button>
        </div>

        <div class="flex-1 overflow-y-auto custom-scrollbar p-2">
          <div v-if="notifications.length === 0" class="text-center py-8 text-slate-400">
            <span class="material-symbols-outlined text-3xl mb-2 opacity-50">notifications_paused</span>
            <p class="text-xs">暂无新通知</p>
          </div>

          <div v-else class="space-y-1">
            <div 
              v-for="notif in notifications" 
              :key="notif.id"
              class="p-3 rounded-xl transition-colors flex gap-3 cursor-pointer group hover:bg-white/60 relative"
              :class="{ 'opacity-60': notif.isRead }"
              @click="markRead(notif.id)"
            >
              <div v-if="!notif.isRead" class="absolute left-2 top-1/2 -translate-y-1/2 w-1.5 h-1.5 bg-[#0084ff] rounded-full"></div>
              <div class="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 text-primary group-hover:bg-primary/20 ml-2">
                <span class="material-symbols-outlined text-[16px]">{{ notif.icon }}</span>
              </div>
              <div>
                <p class="text-[13px] text-slate-800 font-medium leading-snug">{{ notif.title }}</p>
                <p class="text-xs text-slate-500 mt-1">{{ notif.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const isOpen = ref(false)
const dropdownRef = ref(null)

const notifications = ref([
  { id: 1, title: '《春日漫步》已自动添加到生活归档。', time: '10 分钟前', icon: 'auto_awesome', isRead: false },
  { id: 2, title: '你本月的周报 "Weekly Review #12" 已经生成完毕。', time: '2 小时前', icon: 'summarize', isRead: false },
  { id: 3, title: '系统更新：全新的 V2.0 搜索与交互面板已上线！', time: '1 天前', icon: 'system_update', isRead: true },
])

const unreadCount = computed(() => notifications.value.filter(n => !n.isRead).length)

const toggle = () => {
  isOpen.value = !isOpen.value
}

const markRead = (id) => {
  const notif = notifications.value.find(n => n.id === id)
  if (notif) notif.isRead = true
}

const markAllRead = () => {
  notifications.value.forEach(n => n.isRead = true)
}

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.98);
}
</style>
