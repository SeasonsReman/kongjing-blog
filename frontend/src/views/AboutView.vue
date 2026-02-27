<template>
  <main class="flex-1 p-6 grid grid-cols-1 lg:grid-cols-12 gap-8 overflow-hidden pb-8">

    <!-- Left: Profile & Skills -->
    <section class="lg:col-span-5 flex flex-col h-full overflow-hidden space-y-8">
      
      <!-- Profile Glass Card -->
      <div class="glass-panel flex-shrink-0 rounded-[2rem] p-8 shadow-lg border border-white/60 relative overflow-hidden flex flex-col items-center text-center">
        <div class="absolute inset-0 bg-gradient-to-br from-white/40 to-white/10 opacity-50 z-0"></div>
        <div class="relative z-10">
          <div class="w-32 h-32 mx-auto rounded-full bg-[#FFBB00] border-4 border-white shadow-xl overflow-hidden mb-6 group cursor-pointer">
            <img src="https://api.dicebear.com/7.x/bottts-neutral/svg?seed=kongying&backgroundColor=transparent" 
                 class="w-full h-full object-contain transition-transform duration-500 group-hover:scale-110" alt="Avatar">
          </div>
          <h1 class="text-3xl font-bold serif-font text-slate-800 mb-2">WINTER 峰昇。</h1>
          <p class="text-sm font-display tracking-widest text-primary/70 uppercase mb-4">Designer & Developer</p>
          <p class="text-slate-600 text-sm leading-relaxed mb-6 italic px-4">
            "黄昏于万物之间，临于天地之时。"
          </p>
          
          <div class="flex justify-center gap-4">
            <a href="#" class="w-10 h-10 rounded-full bg-white/50 border border-white/60 hover:bg-white text-slate-500 hover:text-slate-800 flex items-center justify-center shadow-sm transition-all hover:-translate-y-1">
              <span class="material-symbols-outlined text-[20px]">link</span>
            </a>
            <a href="#" class="w-10 h-10 rounded-full bg-white/50 border border-white/60 hover:bg-white text-slate-500 hover:text-blue-500 flex items-center justify-center shadow-sm transition-all hover:-translate-y-1">
              <span class="material-symbols-outlined text-[20px]">mail</span>
            </a>
            <a href="#" class="w-10 h-10 rounded-full bg-white/50 border border-white/60 hover:bg-white text-slate-500 hover:text-primary flex items-center justify-center shadow-sm transition-all hover:-translate-y-1">
              <span class="material-symbols-outlined text-[20px]">code</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Skills Radar -->
      <div class="glass-panel flex-1 rounded-[2rem] p-8 shadow-sm border border-white/40 flex flex-col relative overflow-hidden">
        <div class="flex items-center gap-2 mb-6">
          <span class="material-symbols-outlined text-primary">psychology</span>
          <span class="text-xs font-semibold tracking-widest text-slate-600 uppercase">EXPERTISE</span>
        </div>
        
        <div class="flex-1 flex flex-col justify-center gap-6">
          <div v-for="skill in skills" :key="skill.name">
            <div class="flex justify-between items-end mb-2">
              <span class="text-sm font-bold text-slate-700 font-display">{{ skill.name }}</span>
              <span class="text-xs text-slate-400 font-mono">{{ skill.value }}%</span>
            </div>
            <div class="h-2 w-full bg-white/50 rounded-full overflow-hidden shadow-inner">
              <div class="h-full bg-gradient-to-r from-primary/50 to-primary rounded-full relative" :style="{ width: `${skill.value}%` }">
                <div class="absolute inset-0 bg-white/20 w-full h-full animate-[shimmer_2s_infinite]"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </section>

    <!-- Right: The Journey Timeline -->
    <section class="lg:col-span-7 flex flex-col h-full overflow-hidden">
      <div class="glass-panel rounded-[2rem] h-full p-8 flex flex-col shadow-lg border border-white/60 relative overflow-hidden bg-white/20 backdrop-blur-xl">
        <div class="flex items-center gap-2 mb-8 relative z-10">
          <span class="material-symbols-outlined text-primary text-2xl">timeline</span>
          <h2 class="text-2xl font-bold serif-font text-slate-800">My Journey</h2>
        </div>

        <div class="flex-1 overflow-y-auto custom-scrollbar relative z-10 pr-4 pb-12">
          <div class="relative wrap w-full pb-8">
            <div class="border-2-2 absolute border-opacity-20 border-slate-400 h-full border" style="left: 20px"></div>
            
            <div 
              v-for="(event, index) in timeline" 
              :key="index"
              class="mb-8 flex justify-between items-center w-full relative group"
            >
              <div class="absolute w-5 h-5 bg-white border-4 border-primary rounded-full left-[11px] group-hover:scale-125 transition-transform z-10"></div>
              <div class="ml-12 bg-white/40 hover:bg-white/70 backdrop-blur-md rounded-2xl p-6 shadow-sm border border-white/50 transition-all w-full relative">
                <!-- Arrow pointing left -->
                <div class="absolute w-3 h-3 bg-white/40 border-t border-l border-white/50 transform -rotate-45 -left-[7px] top-6 group-hover:bg-white/70 transition-colors"></div>
                
                <h3 class="mb-1 font-bold text-slate-800 serif-font text-lg">{{ event.title }}</h3>
                <span class="text-xs tracking-widest text-primary/80 font-display font-medium mb-3 block">{{ event.date }}</span>
                <p class="text-sm text-slate-600 leading-relaxed font-light">{{ event.desc }}</p>
              </div>
            </div>
            
          </div>
        </div>
      </div>
    </section>

  </main>
</template>

<script setup>
const skills = [
  { name: 'Vue & React', value: 92 },
  { name: 'Python / FastAPI', value: 85 },
  { name: 'UI/UX Design', value: 78 },
  { name: 'Generative AI', value: 65 },
]

const timeline = [
  {
    date: '2026 - PRESENT',
    title: '构建「空·境」V2',
    desc: '全面重构个人数字花园，引入极致玻璃态美学，实现全功能博客引擎与动态全屏交互体验。'
  },
  {
    date: '2025 - MID',
    title: '探索生成式 AI 设计',
    desc: '深入研究基于 AI 的设计工作流，参与多个大型协作项目，推动工具与审美的边界。'
  },
  {
    date: '2023 - 2024',
    title: '全栈架构师的觉醒',
    desc: '从纯前端转向全栈，主导了三个复杂的企业级 SaaS 系统架构与核心业务逻辑开发。'
  },
  {
    date: '2021',
    title: '设计与代码的初识',
    desc: '在这个夏天写下了第一行代码，并开始沉迷于像素级完美的 UI 交互实现。'
  }
]
</script>

<style scoped>
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
</style>
