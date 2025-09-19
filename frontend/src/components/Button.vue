<template>
  <button
    :class="[
      'transition font-medium',
      block ? 'w-full' : '',
      type === 'primary' && 'bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl py-2 px-4',
      type === 'secondary' && 'bg-white border border-indigo-600 text-indigo-600 hover:bg-indigo-50 rounded-xl py-2 px-4',
      type === 'text' && 'text-indigo-600 hover:underline text-sm px-2 py-1',
      disabled && 'opacity-60 cursor-not-allowed',
    ]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<script setup>
defineProps({
  type: { type: String, default: 'primary' },
  disabled: { type: Boolean, default: false },
  block: { type: Boolean, default: false },
})
</script> 