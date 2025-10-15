<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">
    <div class="max-w-7xl mx-auto">
      <!-- 页面标题 -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-4">专业心理测评中心</h1>
        <p class="text-lg text-gray-600 mb-2">基于国际标准量表的科学心理评估</p>
        <p class="text-sm text-gray-500">测评结果仅供参考，如有严重心理困扰请寻求专业帮助</p>
      </div>

      <!-- 分类导航 -->
      <div v-if="!currentTest && !testResult" class="mb-8">
        <div class="flex flex-wrap gap-3 justify-center">
          <button
            v-for="(category, key) in categories"
            :key="key"
            @click="selectedCategory = key"
            class="px-6 py-2 rounded-full font-medium transition-all"
            :class="selectedCategory === key ? 'bg-blue-600 text-white shadow-lg' : 'bg-white text-gray-700 hover:bg-gray-100'"
          >
            {{ key }} ({{ category.length }})
          </button>
        </div>
      </div>

      <!-- 测评卡片网格 -->
      <div v-if="!currentTest && !testResult" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        <div
          v-for="test in filteredTests"
          :key="test.key"
          class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all transform hover:-translate-y-1"
        >
          <!-- 卡片头部 -->
          <div class="p-6" :class="getCategoryColor(test.category).bg">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="text-xl font-bold text-white mb-1">{{ test.abbr }}</h3>
                <p class="text-sm text-white/90">{{ test.title }}</p>
              </div>
              <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getCategoryIcon(test.category)"></path>
                </svg>
              </div>
            </div>
            <div class="flex items-center text-white/80 text-xs">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              {{ test.time }}
            </div>
          </div>

          <!-- 卡片内容 -->
          <div class="p-6">
            <p class="text-sm text-gray-600 mb-4 line-clamp-2">{{ test.description }}</p>
            
            <div class="mb-4">
              <span class="inline-block px-3 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                {{ test.category }}
              </span>
            </div>

            <button
              @click="startTest(test.key)"
              class="w-full py-3 px-6 rounded-xl font-semibold transition-all"
              :class="getCategoryColor(test.category).button"
            >
              开始测评
            </button>
          </div>
        </div>
      </div>

      <!-- 测评进行中 -->
      <div v-if="currentTest" class="bg-white rounded-2xl shadow-2xl p-8 max-w-4xl mx-auto">
        <div class="mb-6">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h2 class="text-2xl font-bold text-gray-900">{{ questionnaire.title }}</h2>
              <p class="text-sm text-gray-600 mt-1">{{ questionnaire.description }}</p>
            </div>
            <button
              @click="cancelTest"
              class="text-gray-500 hover:text-gray-700 p-2 rounded-full hover:bg-gray-100 transition"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <!-- 进度条 -->
          <div class="w-full bg-gray-200 rounded-full h-3 mb-4">
            <div
              class="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full transition-all duration-300"
              :style="{ width: `${((currentQuestionIndex + 1) / questionnaire.questions.length) * 100}%` }"
            ></div>
          </div>
          <div class="flex justify-between text-sm text-gray-600">
            <span>问题 {{ currentQuestionIndex + 1 }} / {{ questionnaire.questions.length }}</span>
            <span>{{ Math.round(((currentQuestionIndex + 1) / questionnaire.questions.length) * 100) }}%</span>
          </div>
        </div>

        <!-- 当前问题 -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold text-gray-800 mb-6 leading-relaxed">
            {{ questionnaire.questions[currentQuestionIndex] }}
          </h3>

          <!-- 选项 -->
          <div class="space-y-3">
            <div
              v-for="(option, index) in questionnaire.options"
              :key="index"
              class="flex items-center p-4 border-2 rounded-xl cursor-pointer transition-all"
              :class="selectedAnswer === option.score ? 'border-blue-500 bg-blue-50 shadow-md' : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'"
              @click="selectedAnswer = option.score"
            >
              <div
                class="w-6 h-6 rounded-full border-2 mr-4 flex items-center justify-center flex-shrink-0"
                :class="selectedAnswer === option.score ? 'border-blue-500 bg-blue-500' : 'border-gray-300'"
              >
                <div v-if="selectedAnswer === option.score" class="w-3 h-3 bg-white rounded-full"></div>
              </div>
              <span class="font-medium text-gray-800">{{ option.text }}</span>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex justify-between">
          <button
            v-if="currentQuestionIndex > 0"
            @click="previousQuestion"
            class="px-8 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors font-medium"
          >
            ← 上一题
          </button>
          <div v-else></div>

          <button
            @click="nextQuestion"
            :disabled="selectedAnswer === null"
            class="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow-lg"
          >
            {{ currentQuestionIndex === questionnaire.questions.length - 1 ? '完成测评 ✓' : '下一题 →' }}
          </button>
        </div>
      </div>

      <!-- 测评结果 -->
      <div v-if="testResult" class="bg-white rounded-2xl shadow-2xl p-8 max-w-4xl mx-auto">
        <div class="text-center mb-8">
          <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center"
               :class="getResultColorClass(testResult.color).bg">
            <svg class="w-10 h-10" :class="getResultColorClass(testResult.color).text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h2 class="text-3xl font-bold text-gray-900 mb-2">测评完成</h2>
          <p class="text-gray-600">您的 {{ questionnaire.abbr }} 测评结果</p>
        </div>

        <!-- 主要分数（单一量表） -->
        <div v-if="!testResult.subscores" class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6 mb-6">
          <div class="text-center mb-6">
            <div class="text-5xl font-bold mb-3" :class="getResultColorClass(testResult.color).text">
              {{ testResult.score }}
            </div>
            <div class="text-2xl font-semibold mb-2" :class="getResultColorClass(testResult.color).text">
              {{ testResult.level }}
            </div>
          </div>

          <div class="bg-white rounded-xl p-6 shadow-sm">
            <div class="flex items-start">
              <div class="w-10 h-10 rounded-full flex items-center justify-center mr-4 flex-shrink-0" :class="getResultColorClass(testResult.color).bg">
                <svg class="w-5 h-5" :class="getResultColorClass(testResult.color).text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <div>
                <h3 class="font-semibold text-gray-800 mb-2">专业建议</h3>
                <p class="text-gray-700 leading-relaxed whitespace-pre-line">{{ testResult.suggestion }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 分量表分数 -->
        <div v-if="testResult.subscores" class="space-y-4 mb-6">
          <div
            v-for="(subscore, key) in testResult.subscores"
            :key="key"
            class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6"
          >
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-xl font-bold text-gray-800">{{ subscore.name }}</h3>
              <div class="text-right">
                <div class="text-3xl font-bold" :class="getResultColorClass(subscore.color).text">
                  {{ subscore.score }}
                </div>
                <div class="text-sm font-semibold" :class="getResultColorClass(subscore.color).text">
                  {{ subscore.level }}
                </div>
              </div>
            </div>
            
            <div class="bg-white rounded-xl p-4 shadow-sm">
              <p class="text-gray-700 leading-relaxed text-sm">{{ subscore.advice }}</p>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex flex-col sm:flex-row gap-4">
          <button
            @click="restartTest"
            class="flex-1 px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors font-medium"
          >
            重新测评
          </button>
          <router-link
            to="/psych/choose"
            class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors text-center font-medium"
            @click="resetAll"
          >
            选择其他测评
          </router-link>
          <router-link
            to="/home"
            class="flex-1 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all text-center font-medium shadow-lg"
          >
            返回首页
          </router-link>
        </div>
      </div>

      <!-- 历史测评记录 -->
      <div v-if="testHistory.length > 0 && !currentTest && !testResult" class="bg-white rounded-2xl shadow-lg p-6 max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          最近测评记录
        </h2>
        <div class="space-y-3">
          <div
            v-for="record in testHistory.slice(0, 8)"
            :key="record.id"
            class="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl hover:shadow-md transition"
          >
            <div class="flex items-center space-x-4">
              <div class="w-4 h-4 rounded-full" :class="getScoreColorBg(record.score, record.test_type)"></div>
              <div>
                <div class="font-semibold text-gray-800">{{ getTestTitle(record.test_type) }}</div>
                <div class="text-sm text-gray-600">{{ formatDate(record.date) }}</div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-2xl font-bold" :class="getScoreColorText(record.score, record.test_type)">{{ record.score }}</div>
              <div class="text-xs text-gray-500">{{ getScoreLevel(record.test_type, record.score) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { psychApi } from '../api/index.js'

const userId = localStorage.getItem('user_id')

// 测评状态
const categories = ref({})
const allTests = ref([])
const selectedCategory = ref('全部')
const currentTest = ref('')
const questionnaire = ref({})
const currentQuestionIndex = ref(0)
const selectedAnswer = ref(null)
const answers = ref([])
const testResult = ref(null)
const testHistory = ref([])

// 加载所有分类和量表
const loadCategories = async () => {
  try {
    const data = await psychApi.getCategories()
    categories.value = data
    
    // 收集所有测评
    let tests = []
    for (const [cat, testList] of Object.entries(data)) {
      tests = tests.concat(testList.map(t => ({...t, category: cat})))
    }
    allTests.value = tests
    
    // 添加"全部"分类
    categories.value = { '全部': tests, ...data }
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

// 过滤测评
const filteredTests = computed(() => {
  if (selectedCategory.value === '全部') {
    return allTests.value
  }
  return allTests.value.filter(t => t.category === selectedCategory.value)
})

// 开始测评
const startTest = async (testType) => {
  try {
    const data = await psychApi.getQuestionnaire(testType)
    currentTest.value = testType
    questionnaire.value = data
    currentQuestionIndex.value = 0
    selectedAnswer.value = null
    answers.value = []
    testResult.value = null
  } catch (error) {
    console.error('获取问卷失败:', error)
  }
}

// 取消测评
const cancelTest = () => {
  if (confirm('确定要退出当前测评吗？已答题目将不会保存。')) {
    resetAll()
  }
}

// 重置所有状态
const resetAll = () => {
  currentTest.value = ''
  questionnaire.value = {}
  currentQuestionIndex.value = 0
  selectedAnswer.value = null
  answers.value = []
  testResult.value = null
}

// 上一题
const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    selectedAnswer.value = answers.value[currentQuestionIndex.value] ?? null
  }
}

// 下一题或完成测评
const nextQuestion = async () => {
  if (selectedAnswer.value === null) return

  // 保存当前答案
  answers.value[currentQuestionIndex.value] = selectedAnswer.value

  if (currentQuestionIndex.value === questionnaire.value.questions.length - 1) {
    // 完成测评，提交结果
    await submitTest()
  } else {
    // 下一题
    currentQuestionIndex.value++
    selectedAnswer.value = answers.value[currentQuestionIndex.value] ?? null
  }
}

// 提交测评
const submitTest = async () => {
  try {
    const data = await psychApi.submitTest(userId, currentTest.value, answers.value)
    testResult.value = data
    currentTest.value = ''
    loadTestHistory()
  } catch (error) {
    console.error('提交测评失败:', error)
    alert('提交失败，请重试')
  }
}

// 重新测评
const restartTest = () => {
  testResult.value = null
}

// 加载历史记录
const loadTestHistory = async () => {
  if (!userId) return

  try {
    const data = await psychApi.getHistory(userId)
    testHistory.value = data
  } catch (error) {
    console.error('加载历史记录失败:', error)
  }
}

// 获取分类颜色
const getCategoryColor = (category) => {
  const colors = {
    '情绪与心境': {bg: 'bg-gradient-to-br from-blue-500 to-blue-600', button: 'bg-blue-600 hover:bg-blue-700 text-white'},
    '人际关系': {bg: 'bg-gradient-to-br from-purple-500 to-purple-600', button: 'bg-purple-600 hover:bg-purple-700 text-white'},
    '自我认知': {bg: 'bg-gradient-to-br from-green-500 to-green-600', button: 'bg-green-600 hover:bg-green-700 text-white'},
    '职场与学业': {bg: 'bg-gradient-to-br from-orange-500 to-orange-600', button: 'bg-orange-600 hover:bg-orange-700 text-white'},
    '创伤与应激': {bg: 'bg-gradient-to-br from-red-500 to-red-600', button: 'bg-red-600 hover:bg-red-700 text-white'}
  }
  return colors[category] || {bg: 'bg-gradient-to-br from-gray-500 to-gray-600', button: 'bg-gray-600 hover:bg-gray-700 text-white'}
}

// 获取分类图标
const getCategoryIcon = (category) => {
  const icons = {
    '情绪与心境': 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z',
    '人际关系': 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',
    '自我认知': 'M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z',
    '职场与学业': 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    '创伤与应激': 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'
  }
  return icons[category] || 'M13 10V3L4 14h7v7l9-11h-7z'
}

// 获取结果颜色类
const getResultColorClass = (color) => {
  const colors = {
    'green': {bg: 'bg-green-100', text: 'text-green-600'},
    'yellow': {bg: 'bg-yellow-100', text: 'text-yellow-600'},
    'orange': {bg: 'bg-orange-100', text: 'text-orange-600'},
    'red': {bg: 'bg-red-100', text: 'text-red-600'}
  }
  return colors[color] || {bg: 'bg-gray-100', text: 'text-gray-600'}
}

// 获取分数等级（用于历史记录）
const getScoreLevel = (testType, score) => {
  // 简化逻辑，实际应从后端配置获取
  if (testType === 'PHQ9' || testType === 'GAD7') {
    if (score < 5) return '无/极轻微'
    if (score < 10) return '轻度'
    if (score < 15) return '中度'
    return '重度'
  }
  return ''
}

const getScoreColorBg = (score, testType) => {
  if (testType === 'PHQ9' || testType === 'GAD7') {
    if (score < 5) return 'bg-green-500'
    if (score < 10) return 'bg-yellow-500'
    if (score < 15) return 'bg-orange-500'
    return 'bg-red-500'
  }
  return 'bg-gray-500'
}

const getScoreColorText = (score, testType) => {
  if (testType === 'PHQ9' || testType === 'GAD7') {
    if (score < 5) return 'text-green-600'
    if (score < 10) return 'text-yellow-600'
    if (score < 15) return 'text-orange-600'
    return 'text-red-600'
  }
  return 'text-gray-600'
}

// 获取测评标题
const getTestTitle = (testType) => {
  const test = allTests.value.find(t => t.key === testType)
  return test ? test.abbr : testType
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

onMounted(() => {
  loadCategories()
  loadTestHistory()
})
</script>
