<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- 顶部导航栏 -->
    <nav class="sticky top-0 z-50 glass border-b border-white/20 backdrop-blur-xl">
      <div class="container-custom">
        <div class="flex items-center justify-between h-16">
          <button 
            @click="goBack"
            class="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
            </svg>
            <span class="font-medium">返回</span>
          </button>
          
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">心理测评</h1>
          
          <div class="w-20"></div>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <div class="container-custom py-8">
      <!-- 选择测评（未开始时） -->
      <div v-if="currentStep === 'choose'" class="max-w-6xl mx-auto">
        <div 
          v-motion
          :initial="{ opacity: 0, y: -20 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
          class="text-center mb-12"
        >
          <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            选择 <span class="text-gradient-primary">心理测评</span>
          </h2>
          <p class="text-lg text-gray-600 dark:text-gray-300">
            10种专业量表，全面了解您的心理状态
          </p>
        </div>

        <!-- 分类标签 -->
        <div class="flex justify-center mb-8 space-x-2">
          <button
            v-for="cat in categories"
            :key="cat.id"
            @click="selectedCategory = cat.id"
            :class="[
              'px-6 py-3 rounded-xl font-medium transition-all duration-300',
              selectedCategory === cat.id
                ? 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white shadow-lg scale-105'
                : 'bg-white/50 dark:bg-gray-800/50 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700'
            ]"
          >
            {{ cat.name }}
          </button>
        </div>

        <!-- 测评卡片网格 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="(test, index) in filteredTests"
            :key="test.id"
            v-motion
            :initial="{ opacity: 0, y: 50 }"
            :enter="{ opacity: 1, y: 0, transition: { delay: index * 100, duration: 500 } }"
            @click="selectTest(test)"
            class="group cursor-pointer"
          >
            <div class="glass-card p-6 h-full hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative overflow-hidden">
              <!-- 装饰性背景 -->
              <div class="absolute inset-0 opacity-0 group-hover:opacity-10 transition-opacity duration-300"
                   :style="{ background: `linear-gradient(135deg, ${test.color}, ${test.color2})` }">
              </div>

              <!-- 图标 -->
              <div class="relative z-10 mb-4 flex justify-center">
                <div class="w-16 h-16 rounded-2xl flex items-center justify-center shadow-xl transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-300"
                     :style="{ background: `linear-gradient(135deg, ${test.color}, ${test.color2})` }">
                  <span class="text-3xl">{{ test.icon }}</span>
                </div>
              </div>

              <!-- 测评信息 -->
              <div class="relative z-10 text-center">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
                  {{ test.name }}
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  {{ test.description }}
                </p>
                
                <!-- 信息标签 -->
                <div class="flex justify-center items-center space-x-4 text-xs text-gray-500 dark:text-gray-400 mb-4">
                  <span class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    {{ test.duration }}分钟
                  </span>
                  <span class="flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                    {{ test.questions }}题
                  </span>
                </div>

                <!-- 开始按钮 -->
                <button class="btn btn-primary w-full opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  开始测评
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 测评进行中 -->
      <div v-else-if="currentStep === 'testing'" class="max-w-4xl mx-auto">
        <div class="glass-card p-8">
          <!-- 顶部进度条 -->
          <div class="mb-8">
            <div class="flex justify-between items-center mb-3">
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white">
                {{ selectedTest.name }}
              </h3>
              <span class="text-sm font-medium text-gray-600 dark:text-gray-400">
                {{ currentQuestionIndex + 1 }} / {{ selectedTest.questions }}
              </span>
            </div>
            
            <!-- 进度条 -->
            <div class="relative h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div 
                class="absolute h-full bg-gradient-to-r from-primary-600 to-secondary-600 rounded-full transition-all duration-500 ease-out"
                :style="{ width: `${progress}%` }"
              >
                <!-- 闪光效果 -->
                <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
              </div>
            </div>
            
            <!-- 进度百分比 -->
            <div class="mt-2 text-center">
              <span class="text-sm font-semibold text-primary-600 dark:text-primary-400">
                {{ Math.round(progress) }}% 完成
              </span>
            </div>
          </div>

          <!-- 问题卡片 -->
          <div 
            v-motion
            :initial="{ opacity: 0, x: 50 }"
            :enter="{ opacity: 1, x: 0, transition: { duration: 400 } }"
            :key="currentQuestionIndex"
            class="mb-8"
          >
            <div class="bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 p-6 rounded-2xl border-2 border-primary-200 dark:border-primary-800">
              <p class="text-lg font-medium text-gray-900 dark:text-white leading-relaxed">
                {{ currentQuestion.text }}
              </p>
            </div>
          </div>

          <!-- 选项列表 -->
          <div class="space-y-3 mb-8">
            <button
              v-for="(option, index) in currentQuestion.options"
              :key="index"
              @click="selectAnswer(option.value)"
              :class="[
                'w-full p-5 rounded-xl text-left transition-all duration-300 transform',
                answers[currentQuestionIndex] === option.value
                  ? 'bg-gradient-to-r from-primary-600 to-secondary-600 text-white shadow-xl scale-105 border-2 border-primary-500'
                  : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-700 hover:scale-105 border-2 border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-700'
              ]"
            >
              <div class="flex items-center">
                <div :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center mr-4 font-bold text-sm flex-shrink-0 transition-colors',
                  answers[currentQuestionIndex] === option.value
                    ? 'bg-white/20 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                ]">
                  {{ String.fromCharCode(65 + index) }}
                </div>
                <span class="flex-1 font-medium">{{ option.text }}</span>
                <svg 
                  v-if="answers[currentQuestionIndex] === option.value"
                  class="w-6 h-6 text-white flex-shrink-0 ml-3"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
              </div>
            </button>
          </div>

          <!-- 导航按钮 -->
          <div class="flex justify-between items-center">
            <button
              @click="previousQuestion"
              :disabled="currentQuestionIndex === 0"
              class="btn btn-ghost disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
              上一题
            </button>

            <button
              v-if="currentQuestionIndex < selectedTest.questions - 1"
              @click="nextQuestion"
              :disabled="answers[currentQuestionIndex] === null"
              class="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              下一题
              <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>

            <button
              v-else
              @click="submitTest"
              :disabled="answers[currentQuestionIndex] === null || isSubmitting"
              class="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <svg v-if="isSubmitting" class="animate-spin w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isSubmitting ? '提交中...' : '提交测评' }}
            </button>
          </div>
        </div>

        <!-- 底部提示 -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-500 dark:text-gray-400">
            💡 请根据您的真实感受作答，没有对错之分
          </p>
        </div>
      </div>

      <!-- 结果展示 -->
      <div v-else-if="currentStep === 'result'" class="max-w-5xl mx-auto">
        <div
          v-motion
          :initial="{ opacity: 0, scale: 0.9 }"
          :enter="{ opacity: 1, scale: 1, transition: { duration: 600 } }"
        >
          <!-- 结果卡片 -->
          <div class="glass-card p-8 mb-6">
            <!-- 头部 -->
            <div class="text-center mb-8">
              <div class="w-24 h-24 mx-auto mb-6 rounded-3xl flex items-center justify-center shadow-2xl animate-bounce-in"
                   :style="{ background: `linear-gradient(135deg, ${selectedTest.color}, ${selectedTest.color2})` }">
                <span class="text-5xl">{{ result.level === '轻度' || result.level === '正常' ? '🎉' : result.level === '中度' ? '😊' : '💪' }}</span>
              </div>
              <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-3">
                测评完成！
              </h2>
              <p class="text-lg text-gray-600 dark:text-gray-400">
                {{ selectedTest.name }} · {{ new Date().toLocaleDateString('zh-CN') }}
              </p>
            </div>

            <!-- 得分展示 -->
            <div class="mb-8">
              <div class="text-center mb-4">
                <div class="inline-flex items-baseline space-x-2">
                  <span class="text-6xl font-bold text-gradient-primary">{{ result.score }}</span>
                  <span class="text-2xl text-gray-500 dark:text-gray-400">分</span>
                </div>
              </div>

              <!-- 等级标签 -->
              <div class="flex justify-center mb-6">
                <span 
                  :class="[
                    'px-6 py-3 rounded-full text-lg font-bold shadow-lg',
                    result.level === '正常' || result.level === '轻度' ? 'bg-success-100 text-success-700' :
                    result.level === '中度' ? 'bg-warning-100 text-warning-700' :
                    'bg-danger-100 text-danger-700'
                  ]"
                >
                  {{ result.level }}
                </span>
              </div>

              <!-- 可视化进度条 -->
              <div class="relative h-6 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div 
                  :class="[
                    'absolute h-full rounded-full transition-all duration-1000 ease-out',
                    result.level === '正常' || result.level === '轻度' ? 'bg-gradient-to-r from-success-500 to-success-600' :
                    result.level === '中度' ? 'bg-gradient-to-r from-warning-500 to-warning-600' :
                    'bg-gradient-to-r from-danger-500 to-danger-600'
                  ]"
                  :style="{ width: `${(result.score / 27) * 100}%` }"
                ></div>
              </div>
            </div>

            <!-- 建议 -->
            <div class="bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 p-6 rounded-2xl border-2 border-primary-200 dark:border-primary-800">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <svg class="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
                专业建议
              </h3>
              <p class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line">
                {{ result.suggestion }}
              </p>
            </div>

            <!-- AI报告 -->
            <div v-if="result.ai_report" class="mt-6 bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 p-6 rounded-2xl border-2 border-purple-200 dark:border-purple-800">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <svg class="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
                AI 专业评估报告
              </h3>
              <div class="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-line prose dark:prose-invert max-w-none">
                {{ result.ai_report }}
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-center space-x-4">
            <button @click="goBack" class="btn btn-ghost">
              返回首页
            </button>
            <button @click="resetTest" class="btn btn-primary">
              再测一次
            </button>
            <button @click="viewHistory" class="btn btn-secondary">
              查看历史
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 当前步骤
const currentStep = ref('choose') // choose, testing, result

// 分类
const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'emotion', name: '情绪' },
  { id: 'personality', name: '人格' },
  { id: 'stress', name: '压力' }
])

const selectedCategory = ref('all')

// 测评列表
const tests = ref([
  {
    id: 'PHQ9',
    name: 'PHQ-9 抑郁量表',
    description: '评估抑郁症状的严重程度',
    category: 'emotion',
    icon: '😔',
    color: '#8b5cf6',
    color2: '#a78bfa',
    duration: 3,
    questions: 9
  },
  {
    id: 'GAD7',
    name: 'GAD-7 焦虑量表',
    description: '评估焦虑症状的严重程度',
    category: 'emotion',
    icon: '😰',
    color: '#06b6d4',
    color2: '#22d3ee',
    duration: 3,
    questions: 7
  },
  {
    id: 'PSS14',
    name: 'PSS-14 压力量表',
    description: '评估压力感知水平',
    category: 'stress',
    icon: '😤',
    color: '#10b981',
    color2: '#34d399',
    duration: 5,
    questions: 14
  },
  {
    id: 'PANAS',
    name: 'PANAS 情绪量表',
    description: '评估积极和消极情绪',
    category: 'emotion',
    icon: '😊',
    color: '#f59e0b',
    color2: '#fbbf24',
    duration: 5,
    questions: 20
  },
  {
    id: 'ECR36',
    name: 'ECR-36 依恋量表',
    description: '评估依恋风格',
    category: 'personality',
    icon: '💑',
    color: '#ec4899',
    color2: '#f472b6',
    duration: 10,
    questions: 36
  },
  {
    id: 'IRI28',
    name: 'IRI-28 共情量表',
    description: '评估共情能力',
    category: 'personality',
    icon: '🤝',
    color: '#8b5cf6',
    color2: '#a78bfa',
    duration: 8,
    questions: 28
  },
  {
    id: 'RSES',
    name: 'RSES 自尊量表',
    description: '评估自尊水平',
    category: 'personality',
    icon: '💪',
    color: '#06b6d4',
    color2: '#22d3ee',
    duration: 3,
    questions: 10
  },
  {
    id: 'SCS26',
    name: 'SCS-26 自我同情量表',
    description: '评估自我同情能力',
    category: 'personality',
    icon: '🌻',
    color: '#10b981',
    color2: '#34d399',
    duration: 8,
    questions: 26
  },
  {
    id: 'MBI22',
    name: 'MBI-22 职业倦怠量表',
    description: '评估职业倦怠程度',
    category: 'stress',
    icon: '😫',
    color: '#f59e0b',
    color2: '#fbbf24',
    duration: 8,
    questions: 22
  },
  {
    id: 'PCL5',
    name: 'PCL-5 创伤后应激量表',
    description: '评估PTSD症状',
    category: 'stress',
    icon: '😨',
    color: '#ec4899',
    color2: '#f472b6',
    duration: 6,
    questions: 20
  }
])

// 筛选后的测评
const filteredTests = computed(() => {
  if (selectedCategory.value === 'all') {
    return tests.value
  }
  return tests.value.filter(test => test.category === selectedCategory.value)
})

// 选中的测评
const selectedTest = ref(null)

// 当前问题索引
const currentQuestionIndex = ref(0)

// 答案数组
const answers = ref([])

// 测评问题（示例）
const questionsList = ref([])

// 当前问题
const currentQuestion = computed(() => {
  return questionsList.value[currentQuestionIndex.value] || {}
})

// 进度
const progress = computed(() => {
  return ((currentQuestionIndex.value + 1) / selectedTest.value.questions) * 100
})

// 提交状态
const isSubmitting = ref(false)

// 测评结果
const result = ref(null)

// 用户ID
const userId = localStorage.getItem('user_id')

// 选择测评
const selectTest = async (test) => {
  selectedTest.value = test
  currentStep.value = 'testing'
  currentQuestionIndex.value = 0
  answers.value = Array(test.questions).fill(null)
  
  // 加载问卷
  await loadQuestionnaire(test.id)
}

// 加载问卷
const loadQuestionnaire = async (testType) => {
  try {
    const response = await fetch(`/api/psych/questionnaire?test_type=${testType}`)
    if (response.ok) {
      const data = await response.json()
      questionsList.value = data.questions
    }
  } catch (error) {
    console.error('加载问卷失败:', error)
    questionsList.value = generateMockQuestions(selectedTest.value.questions)
  }
}

// 生成模拟问题
const generateMockQuestions = (count) => {
  return Array(count).fill(null).map((_, i) => ({
    text: `第 ${i + 1} 题：请根据您的实际情况选择`,
    options: [
      { text: '完全不符合', value: 0 },
      { text: '偶尔符合', value: 1 },
      { text: '有时符合', value: 2 },
      { text: '经常符合', value: 3 },
      { text: '总是符合', value: 4 }
    ]
  }))
}

// 选择答案
const selectAnswer = (value) => {
  answers.value[currentQuestionIndex.value] = value
}

// 下一题
const nextQuestion = () => {
  if (currentQuestionIndex.value < selectedTest.value.questions - 1) {
    currentQuestionIndex.value++
  }
}

// 上一题
const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

// 提交测评
const submitTest = async () => {
  isSubmitting.value = true
  
  try {
    const response = await fetch('/api/psych/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: parseInt(userId),
        test_type: selectedTest.value.id,
        answers: answers.value
      }),
    })

    if (response.ok) {
      const data = await response.json()
      result.value = data
      currentStep.value = 'result'
    } else {
      throw new Error('提交失败')
    }
  } catch (error) {
    console.error('提交测评失败:', error)
    alert('提交失败，请稍后重试')
  } finally {
    isSubmitting.value = false
  }
}

// 重置测评
const resetTest = () => {
  currentStep.value = 'choose'
  selectedTest.value = null
  currentQuestionIndex.value = 0
  answers.value = []
  result.value = null
}

// 查看历史
const viewHistory = () => {
  // TODO: 实现历史记录页面
  alert('历史记录功能开发中')
}

// 返回
const goBack = () => {
  if (currentStep.value === 'testing') {
    if (confirm('确定要放弃当前测评吗？')) {
      resetTest()
    }
  } else {
    router.push('/home')
  }
}

onMounted(() => {
  // 初始化
})
</script>

<style scoped>
/* 自定义样式 */
.prose {
  @apply text-gray-700 dark:text-gray-300;
}
</style>

