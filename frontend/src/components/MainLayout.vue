<template>
  <div class="min-h-screen bg-[#EDF3FF] flex">
    <!-- Mobile drawer -->
    <transition name="fade">
      <div v-if="open" class="fixed inset-0 z-40 bg-black/30 md:hidden" @click="toggle"></div>
    </transition>
    <transition name="slide">
      <div v-if="open" class="fixed inset-y-0 left-0 z-50 w-64 md:hidden shadow-xl">
        <Sidebar />
      </div>
    </transition>

    <!-- Desktop sidebar -->
    <Sidebar class="hidden md:block" />

    <!-- Main content -->
    <div class="flex-1 min-w-0 flex flex-col">
      <Header @toggle="toggle" />
      <main class="flex-1 w-full max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-6">
        <slot />
      </main>
      <Footer />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from './Header.vue'
import Footer from './Footer.vue'
import Sidebar from './Sidebar.vue'
const open = ref(false)
function toggle() { open.value = !open.value }
</script>

<style scoped>
.fade-enter-active,.fade-leave-active{transition:opacity .2s}
.fade-enter-from,.fade-leave-to{opacity:0}
.slide-enter-active,.slide-leave-active{transition:transform .2s}
.slide-enter-from{transform:translateX(-100%)}
.slide-leave-to{transform:translateX(-100%)}
</style>


