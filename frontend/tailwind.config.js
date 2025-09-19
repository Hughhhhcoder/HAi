/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          primary: {
            DEFAULT: '#4F46E5', // Indigo 主色
            light: '#6366F1', // 辅助 Indigo
            dark: '#3730A3',
          },
          bg: {
            DEFAULT: '#EDF3FF', // 主背景
            card: '#FFFFFF', // 白色面板
          },
          gray: {
            900: '#1F2937', // 主文字
            700: '#4B5563', // 次文字
            400: '#9CA3AF', // 占位
          },
          indigo: {
            600: '#4F46E5',
            500: '#6366F1',
            100: '#C7D2FE', // 阴影色
          },
          red: {
            500: '#EF4444', // 警告
            50: '#FEF2F2',
          },
        },
        fontFamily: {
          sans: ['Inter', 'Noto Sans SC', 'Plus Jakarta Sans', 'ui-sans-serif', 'system-ui'],
        },
        boxShadow: {
          'indigo-card': '0 4px 24px 0 rgba(199, 210, 254, 0.3)',
          'indigo-sm': '0 2px 8px 0 rgba(199, 210, 254, 0.15)',
        },
        borderRadius: {
          '2xl': '1rem',
          'xl': '0.75rem',
        },
        maxWidth: {
          '7xl': '80rem',
        },
      },
    },
    plugins: [],
  }