<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
    <div class="container-custom py-20">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">测试页面</h1>
      
      <!-- 测试图标大小 -->
      <div class="flex items-center space-x-4 mb-8">
        <div class="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
          </svg>
        </div>
        <span class="text-xl font-semibold text-gray-700">正常大小的图标</span>
      </div>
      
      <!-- 测试按钮 -->
      <div class="flex space-x-4 mb-8">
        <button class="btn btn-primary">主要按钮</button>
        <button class="btn btn-secondary">次要按钮</button>
        <button class="btn btn-ghost">幽灵按钮</button>
      </div>
      
      <!-- 测试卡片 -->
      <div class="glass-card max-w-md">
        <h3 class="text-xl font-bold text-gray-900 mb-4">玻璃态卡片</h3>
        <p class="text-gray-600 mb-4">这是一个测试卡片，用来验证样式是否正确应用。</p>
        <button class="btn btn-primary w-full">测试按钮</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TestPage'
}
</script>
