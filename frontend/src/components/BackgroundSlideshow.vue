<template>
  <div class="fixed inset-0 z-[-1] overflow-hidden bg-black">
    <transition-group name="fade" tag="div">
      <div
        v-for="(bg, index) in backgrounds"
        :key="bg"
        v-show="currentIndex === index"
        class="absolute inset-[-5%] bg-cover bg-center bg-no-repeat w-[110%] h-[110%]"
        :style="{ backgroundImage: `url(${bg})` }"
      ></div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const backgrounds = [
  '/bg_dipingxian.jpg',
  '/bg_bingdao.jpg',
  '/bg_bochuan.jpg',
  '/bg_xihu.jpg'
]

const currentIndex = ref(0)
let intervalId = null

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % backgrounds.length
}

onMounted(() => {
  // Change background every 12 seconds
  intervalId = setInterval(nextSlide, 12000)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 3s ease-in-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
