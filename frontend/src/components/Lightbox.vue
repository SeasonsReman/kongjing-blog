<template>
  <Teleport to="body">
    <Transition name="lightbox">
      <div v-if="modelValue" class="fixed inset-0 z-[200] flex items-center justify-center p-4 sm:p-8" @click.self="close">
        
        <!-- Dark backdrop with strong blur -->
        <div class="absolute inset-0 bg-slate-900/90 backdrop-blur-xl" @click="close"></div>
        
        <!-- Close button -->
        <button @click="close" class="absolute top-6 right-6 z-50 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 text-white backdrop-blur-md flex items-center justify-center transition-all hover:scale-110">
          <span class="material-symbols-outlined text-2xl">close</span>
        </button>

        <!-- Navigation (Left) -->
        <button v-if="hasPrev" @click.stop="prev" class="absolute left-6 top-1/2 -translate-y-1/2 z-50 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 text-white backdrop-blur-md flex items-center justify-center transition-all hover:scale-110 hover:-translate-x-1">
          <span class="material-symbols-outlined text-3xl">chevron_left</span>
        </button>

        <!-- Navigation (Right) -->
        <button v-if="hasNext" @click.stop="next" class="absolute right-6 top-1/2 -translate-y-1/2 z-50 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 text-white backdrop-blur-md flex items-center justify-center transition-all hover:scale-110 hover:translate-x-1">
          <span class="material-symbols-outlined text-3xl">chevron_right</span>
        </button>

        <!-- Image Container -->
        <div class="relative z-10 max-w-7xl max-h-full flex flex-col items-center justify-center space-y-4" @click.stop>
          <Transition name="fade" mode="out-in">
            <img 
              :key="currentImage.url" 
              :src="currentImage.url" 
              class="max-w-full max-h-[80vh] object-contain rounded-lg shadow-2xl ring-1 ring-white/20"
              alt="Lightbox Image" 
            />
          </Transition>
          
          <div class="text-center bg-black/50 backdrop-blur-sm px-6 py-3 rounded-2xl w-fit max-w-2xl px-8 border border-white/10">
            <p v-if="currentImage.caption" class="text-white/90 text-sm md:text-base font-medium">{{ currentImage.caption }}</p>
            <p v-if="currentImage.info" class="text-white/50 text-xs mt-1 font-display tracking-wider uppercase">{{ currentImage.info }}</p>
          </div>
        </div>

      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  images: { type: Array, required: true },
  currentIndex: { type: Number, default: 0 }
})

const emit = defineEmits(['update:modelValue', 'update:currentIndex'])

const currentImage = computed(() => props.images[props.currentIndex] || {})
const hasPrev = computed(() => props.currentIndex > 0)
const hasNext = computed(() => props.currentIndex < props.images.length - 1)

const close = () => {
  emit('update:modelValue', false)
}

const prev = () => {
  if (hasPrev.value) {
    emit('update:currentIndex', props.currentIndex - 1)
  }
}

const next = () => {
  if (hasNext.value) {
    emit('update:currentIndex', props.currentIndex + 1)
  }
}

const handleKeydown = (e) => {
  if (!props.modelValue) return
  if (e.key === 'Escape') close()
  if (e.key === 'ArrowLeft') prev()
  if (e.key === 'ArrowRight') next()
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

watch(() => props.modelValue, (isOpen) => {
  if (isOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})
</script>

<style scoped>
.lightbox-enter-active,
.lightbox-leave-active {
  transition: opacity 0.4s ease;
}

.lightbox-enter-from,
.lightbox-leave-to {
  opacity: 0;
}

.lightbox-enter-active img {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.lightbox-enter-from img {
  opacity: 0;
  transform: scale(0.95) translateY(20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: scale(0.98);
}
.fade-leave-to {
  opacity: 0;
  transform: scale(1.02);
}
</style>
