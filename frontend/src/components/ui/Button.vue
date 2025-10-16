<template>
  <component
    :is="tag"
    :type="tag === 'button' ? nativeType : undefined"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <!-- Loading Spinner -->
    <svg
      v-if="loading"
      class="animate-spin h-5 w-5 mr-2"
      :class="iconSize"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      ></circle>
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>

    <!-- Icon (left) -->
    <span v-if="$slots.icon && !loading" class="mr-2" :class="iconSize">
      <slot name="icon" />
    </span>

    <!-- Content -->
    <span><slot /></span>

    <!-- Icon (right) -->
    <span v-if="$slots.iconRight" class="ml-2" :class="iconSize">
      <slot name="iconRight" />
    </span>

    <!-- Ripple Effect -->
    <span
      v-if="ripple && !disabled"
      class="absolute inset-0 overflow-hidden rounded-inherit pointer-events-none"
    >
      <span
        v-for="(r, i) in ripples"
        :key="i"
        class="absolute bg-white/30 rounded-full animate-ripple"
        :style="{
          left: `${r.x}px`,
          top: `${r.y}px`,
          width: '20px',
          height: '20px',
        }"
      />
    </span>
  </component>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  // 变体
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'warning', 'danger', 'ghost', 'outline', 'link'].includes(value),
  },
  // 尺寸
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value),
  },
  // 标签类型
  tag: {
    type: String,
    default: 'button',
  },
  // 原生类型
  nativeType: {
    type: String,
    default: 'button',
  },
  // 禁用
  disabled: {
    type: Boolean,
    default: false,
  },
  // 加载中
  loading: {
    type: Boolean,
    default: false,
  },
  // 全宽
  block: {
    type: Boolean,
    default: false,
  },
  // 圆形
  rounded: {
    type: Boolean,
    default: false,
  },
  // Ripple 效果
  ripple: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['click'])

const ripples = ref([])

const buttonClasses = computed(() => {
  const base = [
    'relative inline-flex items-center justify-center',
    'font-semibold transition-all duration-300 ease-out',
    'focus:outline-none focus:ring-4',
    'disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none',
    'overflow-hidden',
  ]

  // 尺寸
  const sizeClasses = {
    xs: 'px-2.5 py-1.5 text-xs',
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-base',
    lg: 'px-6 py-3 text-lg',
    xl: 'px-8 py-4 text-xl',
  }

  // 变体
  const variantClasses = {
    primary: [
      'bg-gradient-to-r from-primary-600 to-primary-700',
      'hover:from-primary-700 hover:to-primary-800',
      'text-white shadow-lg hover:shadow-xl',
      'focus:ring-primary-500/50',
    ],
    secondary: [
      'bg-gradient-to-r from-secondary-500 to-secondary-600',
      'hover:from-secondary-600 hover:to-secondary-700',
      'text-white shadow-lg hover:shadow-xl',
      'focus:ring-secondary-500/50',
    ],
    success: [
      'bg-gradient-to-r from-success-500 to-success-600',
      'hover:from-success-600 hover:to-success-700',
      'text-white shadow-lg hover:shadow-xl',
      'focus:ring-success-500/50',
    ],
    warning: [
      'bg-gradient-to-r from-warning-500 to-warning-600',
      'hover:from-warning-600 hover:to-warning-700',
      'text-white shadow-lg hover:shadow-xl',
      'focus:ring-warning-500/50',
    ],
    danger: [
      'bg-gradient-to-r from-danger-500 to-danger-600',
      'hover:from-danger-600 hover:to-danger-700',
      'text-white shadow-lg hover:shadow-xl',
      'focus:ring-danger-500/50',
    ],
    ghost: [
      'bg-transparent hover:bg-gray-100',
      'text-gray-700 hover:text-gray-900',
      'focus:ring-gray-500/50',
    ],
    outline: [
      'bg-transparent border-2 border-primary-600',
      'hover:bg-primary-50',
      'text-primary-600 hover:text-primary-700',
      'focus:ring-primary-500/50',
    ],
    link: [
      'bg-transparent',
      'text-primary-600 hover:text-primary-700 hover:underline',
      'focus:ring-primary-500/50',
      'shadow-none',
    ],
  }

  // 圆角
  const roundedClasses = props.rounded ? 'rounded-full' : 'rounded-xl'

  // 全宽
  const blockClasses = props.block ? 'w-full' : ''

  // Hover 效果
  const hoverClasses = !props.disabled && !props.loading ? 'hover:-translate-y-0.5 active:translate-y-0' : ''

  return [
    ...base,
    sizeClasses[props.size],
    ...(Array.isArray(variantClasses[props.variant]) ? variantClasses[props.variant] : [variantClasses[props.variant]]),
    roundedClasses,
    blockClasses,
    hoverClasses,
  ].join(' ')
})

const iconSize = computed(() => {
  const sizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-7 h-7',
  }
  return sizes[props.size]
})

const handleClick = (event) => {
  if (props.disabled || props.loading) return

  // Ripple effect
  if (props.ripple) {
    const rect = event.currentTarget.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top

    ripples.value.push({ x, y })

    setTimeout(() => {
      ripples.value.shift()
    }, 600)
  }

  emit('click', event)
}
</script>

<style scoped>
.rounded-inherit {
  border-radius: inherit;
}
</style>

