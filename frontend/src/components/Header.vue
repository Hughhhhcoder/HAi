<template>
  <header class="w-full bg-white/90 backdrop-blur shadow-sm shadow-indigo-100/30 sticky top-0 z-30">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <button class="md:hidden p-2 rounded-lg hover:bg-gray-100" @click="$emit('toggle')" aria-label="Open Menu">
          <svg class="w-5 h-5 text-gray-700" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
        <img src="/logo.svg" alt="logo" class="h-7" />
      </div>
      <div class="flex items-center space-x-3">
        <div class="hidden md:flex items-center space-x-1 text-sm text-gray-600">
          <router-link class="px-3 py-1.5 rounded-lg hover:bg-gray-100" to="/home">首页</router-link>
          <router-link class="px-3 py-1.5 rounded-lg hover:bg-gray-100" to="/ai/roles">AI</router-link>
          <router-link class="px-3 py-1.5 rounded-lg hover:bg-gray-100" to="/psych/choose">测评</router-link>
        </div>
        <div class="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold">U</div>
      </div>
    </div>
  </header>
</template>