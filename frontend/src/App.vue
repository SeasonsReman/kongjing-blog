<template>
  <div class="relative min-h-screen w-full overflow-hidden bg-background-light text-slate-900">
    <!-- Animated Background Layer -->
    <div class="fixed inset-0 z-0 w-full h-full pointer-events-none overflow-hidden bg-gradient-to-br from-[#fdfbfb] via-[#e2d1c3] to-[#f4d4ce]">
      <!-- Animated Sunset Clouds Image (Soft Pastel) -->
      <div 
        class="absolute inset-[-10%] w-[120%] h-[120%] bg-cover bg-center bg-no-repeat opacity-80 mix-blend-multiply animate-drift"
        style="background-image: url('https://images.unsplash.com/photo-1500534623283-312aade485b7?q=80&w=2500')"
      ></div>
      
      <!-- Gradient Overlays for Depth and Glassmorphism feel -->
      <div class="absolute inset-0 bg-gradient-to-t from-white/60 via-white/20 to-transparent"></div>
      <div class="absolute inset-0 bg-gradient-to-r from-orange-100/20 via-transparent to-purple-100/20 mix-blend-overlay"></div>
    </div>

    <!-- App Shell -->
    <div class="relative z-10 flex h-screen w-full flex-col">
      <AppNavbar />
      <router-view />
    </div>
  </div>
</template>

<script setup>
import AppNavbar from '@/components/AppNavbar.vue'
</script>

<style>
@keyframes drift {
  0% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(-2%, 1%) scale(1.05);
  }
  66% {
    transform: translate(1%, -2%) scale(1.02);
  }
  100% {
    transform: translate(0, 0) scale(1);
  }
}

.animate-drift {
  animation: drift 40s ease-in-out infinite;
}
</style>
