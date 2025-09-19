<template>
  <div :class="[
    'flex',
    from === 'ai' ? 'justify-start' : 'justify-end',
    'mb-2'
  ]">
    <div :class="[
      'max-w-[70%] px-4 py-3',
      from === 'ai'
        ? 'bg-white text-gray-800 rounded-2xl rounded-br-2xl shadow-indigo-sm'
        : 'bg-indigo-600 text-white rounded-2xl rounded-bl-2xl',
      'shadow'
    ]">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  from: { type: String, default: 'ai' }, // 'ai' or 'user'
})
</script> 