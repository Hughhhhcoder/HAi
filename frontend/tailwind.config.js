import colors from 'tailwindcss/colors'

/** @type {import('tailwindcss').Config} */
export default {
    content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
    ],
    theme: {
      extend: {
      // 🎨 高级配色系统 - 灵感来自现代设计系统
        colors: {
        // 主色调 - 深邃紫罗兰（Violet）
          primary: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          950: '#2e1065',
        },
        // 次要色 - 青色（Cyan）
        secondary: {
          50: '#ecfeff',
          100: '#cffafe',
          200: '#a5f3fc',
          300: '#67e8f9',
          400: '#22d3ee',
          500: '#06b6d4',
          600: '#0891b2',
          700: '#0e7490',
          800: '#155e75',
          900: '#164e63',
          950: '#083344',
        },
        // 强调色 - 粉红（Pink）
        accent: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ec4899',
          600: '#db2777',
          700: '#be185d',
          800: '#9d174d',
          900: '#831843',
          950: '#500724',
        },
        // 成功色
        success: colors.emerald,
        // 警告色
        warning: colors.amber,
        // 错误色
        danger: colors.rose,
        // 信息色
        info: colors.blue,
        // 中性色 - 现代灰
        gray: colors.slate,
      },

      // 📐 间距系统扩展
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '100': '25rem',
        '112': '28rem',
        '128': '32rem',
        '144': '36rem',
      },

      // 🔤 字体系统
      fontFamily: {
        sans: [
          'Inter var',
          'SF Pro Display',
          '-apple-system',
          'BlinkMacSystemFont',
          'system-ui',
          'sans-serif',
        ],
        mono: [
          'JetBrains Mono',
          'Fira Code',
          'Menlo',
          'Monaco',
          'Courier New',
          'monospace',
        ],
        display: [
          'Cal Sans',
          'SF Pro Display',
          'Inter',
          'sans-serif',
        ],
      },

      // 📏 圆角系统
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
        '6xl': '3rem',
      },

      // 🎭 阴影系统 - 更加柔和和真实
      boxShadow: {
        'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
        'DEFAULT': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
        'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
        '2xl': '0 25px 50px -12px rgb(0 0 0 / 0.25)',
        'inner': 'inset 0 2px 4px 0 rgb(0 0 0 / 0.05)',
        // 自定义阴影
        'glow': '0 0 20px rgb(139 92 246 / 0.5)',
        'glow-lg': '0 0 40px rgb(139 92 246 / 0.6)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        'neumorphic': '12px 12px 24px #d1d9e6, -12px -12px 24px #ffffff',
        'neumorphic-inset': 'inset 6px 6px 12px #d1d9e6, inset -6px -6px 12px #ffffff',
      },

      // ✨ 动画系统 - 大幅扩展
      keyframes: {
        // 淡入淡出
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'fade-out': {
          '0%': { opacity: '1' },
          '100%': { opacity: '0' },
        },

        // 滑动动画
        'slide-in-up': {
          '0%': { transform: 'translateY(100%)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'slide-in-down': {
          '0%': { transform: 'translateY(-100%)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        'slide-in-left': {
          '0%': { transform: 'translateX(-100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        'slide-in-right': {
          '0%': { transform: 'translateX(100%)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },

        // 缩放动画
        'scale-in': {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        'scale-out': {
          '0%': { transform: 'scale(1)', opacity: '1' },
          '100%': { transform: 'scale(0.9)', opacity: '0' },
        },

        // 弹跳动画
        'bounce-in': {
          '0%': { transform: 'scale(0.3)', opacity: '0' },
          '50%': { transform: 'scale(1.05)' },
          '70%': { transform: 'scale(0.9)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },

        // 旋转动画
        'spin-slow': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },

        // 脉冲动画
        'pulse-glow': {
          '0%, 100%': { opacity: '1', boxShadow: '0 0 20px rgb(139 92 246 / 0.5)' },
          '50%': { opacity: '0.8', boxShadow: '0 0 40px rgb(139 92 246 / 0.8)' },
        },

        // 浮动动画
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        'float-slow': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },

        // 摇摆动画
        'wiggle': {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' },
        },
        'shake': {
          '0%, 100%': { transform: 'translateX(0)' },
          '10%, 30%, 50%, 70%, 90%': { transform: 'translateX(-10px)' },
          '20%, 40%, 60%, 80%': { transform: 'translateX(10px)' },
        },

        // 渐变动画
        'gradient': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'gradient-x': {
          '0%, 100%': { backgroundPosition: 'left center' },
          '50%': { backgroundPosition: 'right center' },
        },
        'gradient-y': {
          '0%, 100%': { backgroundPosition: 'center top' },
          '50%': { backgroundPosition: 'center bottom' },
        },
        'gradient-xy': {
          '0%, 100%': { backgroundPosition: 'left top' },
          '25%': { backgroundPosition: 'right top' },
          '50%': { backgroundPosition: 'right bottom' },
          '75%': { backgroundPosition: 'left bottom' },
        },

        // 闪烁动画
        'shimmer': {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },

        // 打字动画
        'typing': {
          '0%': { width: '0' },
          '100%': { width: '100%' },
        },
        'blink': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },

        // 进度条动画
        'progress': {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },

        // 加载点动画
        'dots': {
          '0%, 20%': { content: '"."' },
          '40%': { content: '".."' },
          '60%, 100%': { content: '"..."' },
        },

        // Ripple 波纹动画
        'ripple': {
          '0%': { transform: 'scale(0)', opacity: '1' },
          '100%': { transform: 'scale(4)', opacity: '0' },
        },

        // 心跳动画
        'heartbeat': {
          '0%, 100%': { transform: 'scale(1)' },
          '10%, 30%': { transform: 'scale(1.1)' },
          '20%, 40%': { transform: 'scale(1)' },
        },

        // 旋转光环
        'rotate-halo': {
          '0%': { transform: 'rotate(0deg) scale(1)' },
          '50%': { transform: 'rotate(180deg) scale(1.1)' },
          '100%': { transform: 'rotate(360deg) scale(1)' },
        },

        // 滚动提示
        'scroll-indicator': {
          '0%, 100%': { transform: 'translateY(0)', opacity: '0.3' },
          '50%': { transform: 'translateY(10px)', opacity: '1' },
        },

        // 粒子飘动
        'particle-float': {
          '0%, 100%': { transform: 'translate(0, 0) rotate(0deg)' },
          '25%': { transform: 'translate(10px, -10px) rotate(90deg)' },
          '50%': { transform: 'translate(20px, 10px) rotate(180deg)' },
          '75%': { transform: 'translate(10px, 20px) rotate(270deg)' },
        },

        // 展开动画
        'expand': {
          '0%': { transform: 'scale(0.8)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        'collapse': {
          '0%': { transform: 'scale(1)', opacity: '1' },
          '100%': { transform: 'scale(0.8)', opacity: '0' },
        },

        // 弹出动画
        'pop': {
          '0%': { transform: 'scale(0)', opacity: '0' },
          '50%': { transform: 'scale(1.1)', opacity: '1' },
          '100%': { transform: 'scale(1)' },
        },

        // 文字聚焦
        'text-focus': {
          '0%': { filter: 'blur(12px)', opacity: '0' },
          '100%': { filter: 'blur(0px)', opacity: '1' },
        },
      },

      animation: {
        // 基础动画
        'fade-in': 'fade-in 0.5s ease-out',
        'fade-out': 'fade-out 0.5s ease-out',
        'slide-in-up': 'slide-in-up 0.5s ease-out',
        'slide-in-down': 'slide-in-down 0.5s ease-out',
        'slide-in-left': 'slide-in-left 0.5s ease-out',
        'slide-in-right': 'slide-in-right 0.5s ease-out',
        'scale-in': 'scale-in 0.5s ease-out',
        'scale-out': 'scale-out 0.5s ease-out',
        'bounce-in': 'bounce-in 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55)',

        // 循环动画
        'spin-slow': 'spin-slow 3s linear infinite',
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'float-slow': 'float-slow 6s ease-in-out infinite',
        'wiggle': 'wiggle 1s ease-in-out infinite',
        'shake': 'shake 0.5s ease-in-out',

        // 渐变动画
        'gradient': 'gradient 15s ease infinite',
        'gradient-x': 'gradient-x 15s ease infinite',
        'gradient-y': 'gradient-y 15s ease infinite',
        'gradient-xy': 'gradient-xy 15s ease infinite',
        'shimmer': 'shimmer 2s linear infinite',

        // 特殊动画
        'typing': 'typing 3.5s steps(40, end)',
        'blink': 'blink 1s step-end infinite',
        'progress': 'progress 1s ease-in-out infinite',
        'ripple': 'ripple 0.6s linear',
        'heartbeat': 'heartbeat 1.5s ease-in-out infinite',
        'rotate-halo': 'rotate-halo 4s linear infinite',
        'scroll-indicator': 'scroll-indicator 2s ease-in-out infinite',
        'particle-float': 'particle-float 10s ease-in-out infinite',
        'expand': 'expand 0.3s ease-out',
        'collapse': 'collapse 0.3s ease-out',
        'pop': 'pop 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)',
        'text-focus': 'text-focus 1s ease-out',
      },

      // 🌈 背景渐变
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'gradient-mesh': 'linear-gradient(135deg, var(--tw-gradient-stops))',
        'shimmer-gradient': 'linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent)',
      },

      // 🎨 背景大小
      backgroundSize: {
        'auto': 'auto',
        'cover': 'cover',
        'contain': 'contain',
        '200%': '200%',
        '300%': '300%',
        '400%': '400%',
      },

      // ⏱️ 过渡时长
      transitionDuration: {
        '0': '0ms',
        '2000': '2000ms',
        '3000': '3000ms',
        '4000': '4000ms',
        '5000': '5000ms',
      },

      // 📐 宽高
      minHeight: {
        '0': '0',
        'screen': '100vh',
        'screen-90': '90vh',
        'screen-75': '75vh',
        'screen-50': '50vh',
      },

      // 🔢 Z-index
      zIndex: {
        '-1': '-1',
        '60': '60',
        '70': '70',
        '80': '80',
        '90': '90',
        '100': '100',
      },

      // 🎭 Backdrop
      backdropBlur: {
        xs: '2px',
        '3xl': '64px',
        '4xl': '128px',
      },
    },
  },
  plugins: [
    // 自定义插件
    function({ addUtilities, addComponents, theme }) {
      // 玻璃态效果
      addUtilities({
        '.glass': {
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.2)',
        },
        '.glass-dark': {
          background: 'rgba(0, 0, 0, 0.2)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        },
        '.glass-strong': {
          background: 'rgba(255, 255, 255, 0.25)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.3)',
        },

        // 文字渐变
        '.text-gradient': {
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundImage: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        },
        '.text-gradient-primary': {
          backgroundClip: 'text',
          WebkitBackdropFilter: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundImage: `linear-gradient(135deg, ${theme('colors.primary.500')} 0%, ${theme('colors.primary.700')} 100%)`,
        },
        '.text-gradient-secondary': {
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundImage: `linear-gradient(135deg, ${theme('colors.secondary.400')} 0%, ${theme('colors.secondary.600')} 100%)`,
        },
        '.text-gradient-rainbow': {
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundImage: 'linear-gradient(90deg, #667eea, #764ba2, #f093fb, #4facfe)',
          backgroundSize: '300% 100%',
        },

        // 隐藏滚动条
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            display: 'none',
          },
        },

        // 自定义滚动条
        '.scrollbar-thin': {
          '&::-webkit-scrollbar': {
            width: '6px',
            height: '6px',
          },
          '&::-webkit-scrollbar-track': {
            background: theme('colors.gray.100'),
            borderRadius: '10px',
          },
          '&::-webkit-scrollbar-thumb': {
            background: theme('colors.primary.500'),
            borderRadius: '10px',
            '&:hover': {
              background: theme('colors.primary.600'),
            },
          },
        },

        // 平滑滚动
        '.scroll-smooth': {
          scrollBehavior: 'smooth',
        },

        // 3D 变换
        '.transform-3d': {
          transformStyle: 'preserve-3d',
        },

        // 硬件加速
        '.gpu': {
          transform: 'translateZ(0)',
          willChange: 'transform',
        },
      })

      // 添加组件类
      addComponents({
        '.btn-primary': {
          background: `linear-gradient(135deg, ${theme('colors.primary.500')} 0%, ${theme('colors.primary.700')} 100%)`,
          color: 'white',
          padding: `${theme('spacing.3')} ${theme('spacing.6')}`,
          borderRadius: theme('borderRadius.lg'),
          fontWeight: theme('fontWeight.semibold'),
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: theme('boxShadow.lg'),
          },
          '&:active': {
            transform: 'translateY(0)',
          },
        },
        '.card-glass': {
          background: 'rgba(255, 255, 255, 0.1)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          borderRadius: theme('borderRadius.2xl'),
          padding: theme('spacing.6'),
          border: '1px solid rgba(255, 255, 255, 0.2)',
          boxShadow: theme('boxShadow.glass'),
        },
      })
    },
  ],
}
