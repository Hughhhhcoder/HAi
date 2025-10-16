<template>
  <div :class="cardClasses" @click="handleClick">
    <!-- 装饰背景 -->
    <div v-if="decorative" class="absolute inset-0 overflow-hidden rounded-inherit pointer-events-none">
      <div class="absolute -top-24 -right-24 w-48 h-48 bg-primary-500/10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-24 -left-24 w-48 h-48 bg-secondary-500/10 rounded-full blur-3xl"></div>
    </div>

    <!-- 内容 -->
    <div class="relative z-10">
      <!-- 标题区域 -->
      <div v-if="$slots.header || title" :class="headerClasses">
        <slot name="header">
          <h3 :class="titleClasses">{{ title }}</h3>
          <p v-if="subtitle" :class="subtitleClasses">{{ subtitle }}</p>
        </slot>
      </div>

      <!-- 主体内容 -->
      <div :class="bodyClasses">
        <slot />
      </div>

      <!-- 底部区域 -->
      <div v-if="$slots.footer" :class="footerClasses">
        <slot name="footer" />
      </div>
    </div>

    <!-- Hover 遮罩 -->
    <div v-if="hoverable" class="absolute inset-0 bg-gradient-to-br from-primary-500/0 to-secondary-500/0 hover:from-primary-500/5 hover:to-secondary-500/5 rounded-inherit transition-all duration-300 pointer-events-none"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  // 标题
  title: String,
  // 副标题
  subtitle: String,
  // 变体
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'glass', 'gradient', 'bordered', 'elevated'].includes(value),
  },
  // 内边距
  padding: {
    type: String,
    default: 'md',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl'].includes(value),
  },
  // 可悬停
  hoverable: {
    type: Boolean,
    default: false,
  },
  // 可点击
  clickable: {
    type: Boolean,
    default: false,
  },
  // 装饰性背景
  decorative: {
    type: Boolean,
    default: false,
  },
  // 阴影
  shadow: {
    type: String,
    default: 'md',
    validator: (value) => ['none', 'sm', 'md', 'lg', 'xl', '2xl', 'glow'].includes(value),
  },
})

const emit = defineEmits(['click'])

const cardClasses = computed(() => {
  const base = [
    'relative overflow-hidden',
    'transition-all duration-300 ease-out',
  ]

  // 变体样式
  const variantClasses = {
    default: 'bg-white',
    glass: 'glass backdrop-blur-xl bg-white/80',
    gradient: 'bg-gradient-to-br from-primary-50 via-white to-secondary-50',
    bordered: 'bg-white border-2 border-gray-200',
    elevated: 'bg-white',
  }

  // 圆角
  const rounded = 'rounded-2xl'

  // 阴影
  const shadowClasses = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-xl',
    '2xl': 'shadow-2xl',
    glow: 'shadow-glow',
  }

  // Hover 效果
  const hoverClasses = props.hoverable || props.clickable
    ? 'hover:-translate-y-1 hover:shadow-2xl cursor-pointer'
    : ''

  return [
    ...base,
    variantClasses[props.variant],
    rounded,
    shadowClasses[props.shadow],
    hoverClasses,
  ].join(' ')
})

const paddingClasses = computed(() => {
  const paddings = {
    none: 'p-0',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
    xl: 'p-10',
  }
  return paddings[props.padding]
})

const headerClasses = computed(() => {
  return [
    paddingClasses.value,
    props.$slots.default ? 'pb-0' : '',
  ].join(' ')
})

const bodyClasses = computed(() => {
  return paddingClasses.value
})

const footerClasses = computed(() => {
  return [
    paddingClasses.value,
    'pt-0',
  ].join(' ')
})

const titleClasses = 'text-2xl font-bold text-gray-900 mb-1'
const subtitleClasses = 'text-sm text-gray-600'

const handleClick = (event) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
.rounded-inherit {
  border-radius: inherit;
}
</style>

